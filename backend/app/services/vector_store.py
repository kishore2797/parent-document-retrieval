from __future__ import annotations

import uuid
from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.services import embeddings
from app.settings import settings

COLLECTION_NAME = "parent_child_chunks"


def _get_client() -> chromadb.Client:
    if settings.chroma_persist_dir:
        return chromadb.PersistentClient(path=settings.chroma_persist_dir)
    return chromadb.Client(ChromaSettings(anonymized_telemetry=False))


_client: chromadb.Client | None = None


def get_client() -> chromadb.Client:
    global _client
    if _client is None:
        _client = _get_client()
    return _client


def get_collection():
    client = get_client()
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_child_chunks(chunks: list[dict[str, Any]]) -> int:
    """
    Each chunk dict must contain:
    - text: child text
    - metadata: dict including parent_id, doc_id, title, parent_text, child_index, parent_index
    """
    if not chunks:
        return 0
    texts = [c["text"] for c in chunks]
    metadatas = [c.get("metadata", {}) for c in chunks]
    # ensure parent_text exists in metadata
    for meta, txt in zip(metadatas, texts):
        meta.setdefault("text", txt)
    vectors = embeddings.embed_texts(texts)
    ids = [str(uuid.uuid4()) for _ in texts]
    coll = get_collection()
    coll.add(ids=ids, embeddings=vectors, documents=texts, metadatas=metadatas)
    return len(ids)


def query_children(
    query_embedding: list[float],
    top_k: int,
) -> list[dict[str, Any]]:
    coll = get_collection()
    n = coll.count()
    if n == 0:
        return []
    top_k = min(top_k, n)
    res = coll.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    out: list[dict[str, Any]] = []
    ids = res["ids"][0] if res["ids"] else []
    docs = res["documents"][0] if res["documents"] else []
    metas = res["metadatas"][0] if res["metadatas"] else []
    dists = res["distances"][0] if res.get("distances") else []
    for id_, doc, meta, dist in zip(ids, docs, metas, dists or [0] * len(ids)):
        score = 1.0 / (1.0 + float(dist)) if dist is not None else 1.0
        m = meta if isinstance(meta, dict) else {}
        out.append(
            {
                "id": id_,
                "text": doc or m.get("text", ""),
                "score": round(score, 4),
                "metadata": m,
            }
        )
    return out

