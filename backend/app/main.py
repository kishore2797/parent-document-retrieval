from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import documents, query


@asynccontextmanager
async def lifespan(app: FastAPI):
    # No automatic seeding; ingestion happens via API/UI.
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Parent Document Retrieval API",
        version="0.1.0",
        description="Small chunks for retrieval, large parent sections for RAG context.",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    app.include_router(documents.router, prefix="/documents", tags=["documents"])
    app.include_router(query.router, prefix="/query", tags=["query"])

    return app


app = create_app()

