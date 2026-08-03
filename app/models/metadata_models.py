"""
Pydantic models for document metadata (stored in Qdrant payloads).
"""
from pydantic import BaseModel


class ChunkMetadata(BaseModel):
    """Metadata attached to every stored chunk."""

    filename: str
    page_number: int
    chunk_id: str
