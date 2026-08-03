"""
Application settings loaded from environment variables.
All configuration is centralised here — no hardcoded values elsewhere.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pydantic settings model — reads from .env automatically."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- LLM ---
    llm_provider: str = "groq"           # "groq" | "ollama"
    groq_api_key: str = ""
    groq_model: str = "openai/gpt-oss-120b"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"

    # --- Qdrant ---
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_path: str = "./qdrant_storage"   # used for local/embedded mode
    qdrant_use_local: bool = True            # True = embedded local storage
    collection_name: str = "core_rag_collection"

    # --- Embeddings ---
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    vector_size: int = 384

    # --- Chunking ---
    chunk_size: int = 500
    chunk_overlap: int = 100

    # --- Retrieval ---
    top_k: int = 10
    max_context_chunks: int = 5   # kept after re-ranking / trimming

    # --- Prompt ---
    max_context_length: int = 3000   # characters

    # --- API ---
    app_title: str = "RAG Backend API"
    app_version: str = "1.0.0"
    debug: bool = False


# Single global instance – import this everywhere
settings = Settings()
