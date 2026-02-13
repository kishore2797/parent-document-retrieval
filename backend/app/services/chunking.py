from __future__ import annotations

import math
import textwrap
import uuid
from typing import Iterable

from app.settings import settings


def _split_by_length(text: str, max_chars: int) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end
    return [c for c in chunks if c]


def make_parents(doc_id: str, title: str, text: str) -> list[dict]:
    """
    Split raw document text into larger parent sections.
    For simplicity we split by length, but you could use headings/paragraphs.
    """
    parent_texts = _split_by_length(text, settings.parent_max_chars)
    parents: list[dict] = []
    for idx, ptext in enumerate(parent_texts):
        parent_id = f"{doc_id}::p{idx}"
        parents.append(
            {
                "parent_id": parent_id,
                "doc_id": doc_id,
                "title": title,
                "parent_index": idx,
                "text": textwrap.dedent(ptext).strip(),
            }
        )
    return parents


def make_children(parents: Iterable[dict]) -> list[dict]:
    """
    For each parent, create smaller overlapping child chunks for retrieval.
    Returns list of dicts ready for vector_store.add_child_chunks().
    """
    children: list[dict] = []
    max_c = settings.child_max_chars
    overlap = settings.child_overlap_chars

    for parent in parents:
        parent_text: str = parent["text"]
        parent_id: str = parent["parent_id"]
        doc_id: str = parent["doc_id"]
        title: str = parent.get("title") or ""
        parent_index: int = parent.get("parent_index", 0)

        if len(parent_text) <= max_c:
            windows = [parent_text]
        else:
            windows = []
            start = 0
            while start < len(parent_text):
                end = start + max_c
                windows.append(parent_text[start:end])
                start = end - overlap
                if start >= len(parent_text):
                    break

        for child_index, chunk_text in enumerate(windows):
            chunk_text = chunk_text.strip()
            if not chunk_text:
                continue
            children.append(
                {
                    "text": chunk_text,
                    "metadata": {
                        "parent_id": parent_id,
                        "doc_id": doc_id,
                        "title": title,
                        "parent_index": parent_index,
                        "child_index": child_index,
                        "parent_text": parent_text,
                    },
                }
            )

    return children

