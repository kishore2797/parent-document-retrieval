from __future__ import annotations

from collections import defaultdict
from typing import Any

from app.models.schemas import ChildHit, ParentContext
from app.services import embeddings
from app.services.llm import llm_client
from app.services.vector_store import query_children
from app.settings import settings


def retrieve_children(query: str, top_children: int | None = None) -> list[dict[str, Any]]:
    """Embed query and retrieve child chunks from vector store."""
    vec = embeddings.embed_one(query)
    n = top_children or settings.retrieval_children
    return query_children(vec, top_k=n)


def expand_to_parents(
    child_docs: list[dict[str, Any]],
    max_parents: int | None = None,
) -> list[ParentContext]:
    """
    Group child hits by parent_id, aggregate scores, and build parent contexts.
    """
    if not child_docs:
        return []

    by_parent: dict[str, list[dict]] = defaultdict(list)
    for d in child_docs:
        meta = d.get("metadata") or {}
        parent_id = meta.get("parent_id")
        if not parent_id:
            continue
        by_parent[parent_id].append(d)

    parents: list[ParentContext] = []
    for parent_id, docs in by_parent.items():
        # Aggregate score: max child score
        best = max(docs, key=lambda x: x.get("score", 0.0))
        meta = best.get("metadata") or {}
        parent_text = meta.get("parent_text") or ""
        doc_id = meta.get("doc_id") or ""
        title = meta.get("title")
        parents.append(
            ParentContext(
                parent_id=parent_id,
                doc_id=doc_id,
                title=title,
                score=best.get("score", 0.0),
                text=parent_text,
            )
        )

    # Sort parents by descending score
    parents.sort(key=lambda p: p.score, reverse=True)

    # Limit by max_parents and context_max_chars
    limit = max_parents or settings.max_parents
    selected: list[ParentContext] = []
    total_chars = 0
    for p in parents:
        if len(selected) >= limit:
            break
        prospective = total_chars + len(p.text)
        if prospective > settings.context_max_chars and selected:
            break
        selected.append(p)
        total_chars = prospective

    return selected


def build_child_hits(child_docs: list[dict[str, Any]]) -> list[ChildHit]:
    hits: list[ChildHit] = []
    for d in child_docs:
        meta = d.get("metadata") or {}
        hits.append(
            ChildHit(
                id=d.get("id", ""),
                parent_id=meta.get("parent_id", ""),
                doc_id=meta.get("doc_id", ""),
                title=meta.get("title"),
                score=d.get("score", 0.0),
                snippet=d.get("text", ""),
                metadata=meta,
            )
        )
    return hits


RAG_SYSTEM = (
    "You are a helpful assistant answering questions based on provided documents. "
    "Use ONLY the given parent sections as context. If the answer is not present, say so."
)


async def generate_answer(query: str, parents: list[ParentContext]) -> str:
    if not parents:
        return "No relevant parent sections were retrieved."
    context_block = "\n\n".join(
        (f"[{p.title or p.parent_id}]\n{p.text}" if p.title else p.text) for p in parents
    )
    user_prompt = f"Context:\n{context_block}\n\nQuestion: {query}\n\nAnswer:"
    return await llm_client.generate(RAG_SYSTEM, user_prompt)

