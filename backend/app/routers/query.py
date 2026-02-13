from fastapi import APIRouter

from app.models.schemas import QueryRequest, QueryResponse
from app.services.pipeline import (
    build_child_hits,
    expand_to_parents,
    generate_answer,
    retrieve_children,
)

router = APIRouter()


@router.post("", response_model=QueryResponse)
async def query(body: QueryRequest) -> QueryResponse:
    child_docs = retrieve_children(body.query, top_children=body.top_children)
    children = build_child_hits(child_docs)
    parents = expand_to_parents(child_docs, max_parents=body.max_parents)
    answer = None
    if body.generate_answer:
        answer = await generate_answer(body.query, parents)
    return QueryResponse(query=body.query, children=children, parents=parents, answer=answer)

