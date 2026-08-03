"""
Tests for the chunker module.
"""
import pytest
from app.chunking.chunker import chunk_document


SAMPLE_PAGES = [
    {
        "text": "This is the first page of a long document. " * 30,
        "metadata": {"filename": "test.txt", "page_number": 1},
    },
    {
        "text": "Second page content here. " * 20,
        "metadata": {"filename": "test.txt", "page_number": 2},
    },
]


def test_chunk_document_returns_chunks():
    chunks = chunk_document(SAMPLE_PAGES, chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 0


def test_chunk_has_required_keys():
    chunks = chunk_document(SAMPLE_PAGES, chunk_size=200, chunk_overlap=20)
    for chunk in chunks:
        assert "text" in chunk
        assert "metadata" in chunk
        assert "chunk_id" in chunk["metadata"]
        assert "filename" in chunk["metadata"]
        assert "page_number" in chunk["metadata"]


def test_chunk_text_not_empty():
    chunks = chunk_document(SAMPLE_PAGES, chunk_size=200, chunk_overlap=20)
    for chunk in chunks:
        assert chunk["text"].strip() != ""


def test_chunk_ids_are_unique():
    chunks = chunk_document(SAMPLE_PAGES, chunk_size=200, chunk_overlap=20)
    ids = [c["metadata"]["chunk_id"] for c in chunks]
    assert len(ids) == len(set(ids))
