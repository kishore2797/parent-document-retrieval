from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_host: str = "0.0.0.0"
    api_port: int = 8003

    # LLM (OpenAI-compatible) for final answers
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    # Vector store / embeddings
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dimension: int = 384
    chroma_persist_dir: str | None = None  # None = in-memory

    # Chunking
    parent_max_chars: int = 2000  # approximate parent size
    child_max_chars: int = 400    # small chunks for retrieval
    child_overlap_chars: int = 100

    # Retrieval / context
    retrieval_children: int = 30  # how many child hits to consider
    max_parents: int = 4          # how many parents to include in context
    context_max_chars: int = 8000  # rough cap for combined parent text


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

