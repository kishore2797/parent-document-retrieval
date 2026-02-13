from fastapi import APIRouter

from app.models.schemas import IngestRequest, IngestResponse
from app.services.chunking import make_children, make_parents
from app.services.vector_store import add_child_chunks

router = APIRouter()


@router.post("", response_model=IngestResponse, status_code=201)
def ingest_documents(body: IngestRequest) -> IngestResponse:
    all_parents = []
    all_children = []

    for doc in body.documents:
        doc_id = doc.doc_id or f"doc-{hash((doc.title, doc.text)) & 0xFFFFFFFF:x}"
        parents = make_parents(doc_id=doc_id, title=doc.title, text=doc.text)
        children = make_children(parents)
        all_parents.extend(parents)
        all_children.extend(children)

    created_children = add_child_chunks(all_children)

    return IngestResponse(
        parents_created=len(all_parents),
        children_created=created_children,
    )

