"""
Tests for the prompt builder module.
"""
import pytest
from app.prompt.rag_prompt import build_rag_prompt
from app.models.response_models import RetrievedChunk

SAMPLE_CHUNKS = [
    RetrievedChunk(
        text="The capital of France is Paris.",
        score=0.92,
        filename="geography.txt",
        page_number=1,
        chunk_id="abc-123",
    ),
    RetrievedChunk(
        text="Paris is known for the Eiffel Tower.",
        score=0.88,
        filename="travel.pdf",
        page_number=3,
        chunk_id="def-456",
    ),
]


def test_build_prompt_contains_query():
    prompt = build_rag_prompt("What is the capital of France?", SAMPLE_CHUNKS)
    assert "What is the capital of France?" in prompt


def test_build_prompt_contains_context():
    prompt = build_rag_prompt("What is the capital of France?", SAMPLE_CHUNKS)
    assert "Paris" in prompt


def test_build_prompt_empty_query_raises():
    with pytest.raises(ValueError, match="Query must not be empty"):
        build_rag_prompt("", SAMPLE_CHUNKS)


def test_build_prompt_no_chunks_raises():
    with pytest.raises(ValueError, match="No context chunks"):
        build_rag_prompt("Some question?", [])
