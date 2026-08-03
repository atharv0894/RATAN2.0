"""
Pydantic models for API request payloads.
"""
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request body for POST /query."""

    query: str = Field(..., min_length=1, description="User question.")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of chunks to retrieve.")


class IngestURLRequest(BaseModel):
    """Optional future use: ingest by URL."""

    url: str = Field(..., description="URL of the document to ingest.")
