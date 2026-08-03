"""
Pydantic models for API response payloads.
"""
from typing import Any
from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    """A single retrieved chunk with its metadata and score."""

    text: str
    score: float
    filename: str
    page_number: int
    chunk_id: str


class Source(BaseModel):
    """Citation-level metadata for a retrieved source."""

    filename: str
    page_number: int
    chunk_id: str


class RAGResponse(BaseModel):
    """Full structured response returned by POST /query."""

    answer: str
    sources: list[Source]
    retrieved_chunks: list[RetrievedChunk]
    model: str
    provider: str
    latency_ms: float


class IngestResponse(BaseModel):
    """Response for POST /ingest."""

    message: str
    filename: str
    chunks_created: int
    ingestion_time_ms: float


class DocumentListResponse(BaseModel):
    """Response for GET /documents."""

    total: int
    filenames: list[str]


class HealthResponse(BaseModel):
    """Response for GET /health."""

    status: str
    provider: str
    model: str
    qdrant: str
    details: dict[str, Any] = {}
