from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import numpy as np
from sentence_transformers import SentenceTransformer

from app.settings import settings


@lru_cache
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(settings.embedding_model_name)


def embed_texts(texts: Iterable[str]) -> list[list[float]]:
    model = _get_model()
    items = list(texts)
    if not items:
        return []
    embeddings = model.encode(items, batch_size=32, show_progress_bar=False)
    if isinstance(embeddings, np.ndarray):
        return embeddings.tolist()
    return [list(v) for v in embeddings]


def embed_one(text: str) -> list[float]:
    out = embed_texts([text])
    return out[0] if out else []

