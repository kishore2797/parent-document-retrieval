from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ParentDocumentInput(BaseModel):
    title: str = Field(..., description="Human-friendly title or identifier")
    text: str = Field(..., description="Raw document text")
    doc_id: str | None = Field(
        default=None,
        description="Optional stable document id; generated if omitted",
    )


class IngestRequest(BaseModel):
    documents: list[ParentDocumentInput]


class IngestResponse(BaseModel):
    parents_created: int
    children_created: int


class ChildHit(BaseModel):
    id: str
    parent_id: str
    doc_id: str
    title: str | None = None
    score: float
    snippet: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class ParentContext(BaseModel):
    parent_id: str
    doc_id: str
    title: str | None = None
    score: float
    text: str


class QueryRequest(BaseModel):
    query: str
    top_children: int | None = Field(
        default=None,
        description="Override default number of child hits (otherwise use settings.retrieval_children)",
    )
    max_parents: int | None = Field(
        default=None,
        description="Override default number of parents in context",
    )
    generate_answer: bool = True


class QueryResponse(BaseModel):
    query: str
    children: list[ChildHit] = Field(default_factory=list)
    parents: list[ParentContext] = Field(default_factory=list)
    answer: str | None = None

