"""
Integration-style tests for the FastAPI endpoints.
Uses TestClient and mocks the service layer to avoid real IO.
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app
from app.models.response_models import RAGResponse, Source, RetrievedChunk

client = TestClient(app)


MOCK_RAG_RESPONSE = RAGResponse(
    answer="Paris is the capital of France.",
    sources=[Source(filename="geo.txt", page_number=1, chunk_id="abc")],
    retrieved_chunks=[
        RetrievedChunk(
            text="The capital of France is Paris.",
            score=0.95,
            filename="geo.txt",
            page_number=1,
            chunk_id="abc",
        )
    ],
    model="gpt-oss-120b",
    provider="groq",
    latency_ms=123.4,
)


def test_health_endpoint():
    with (
        patch("app.api.routes.health.get_qdrant_client"),
        patch(
            "app.api.routes.health.ProviderFactory.get_provider",
            return_value=type("P", (), {"provider_name": "groq", "model_name": "gpt-oss-120b"})(),
        ),
    ):
        response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_query_endpoint_success():
    with patch("app.api.routes.query.handle_query", return_value=MOCK_RAG_RESPONSE):
        response = client.post("/query", json={"query": "What is the capital of France?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "latency_ms" in data


def test_query_endpoint_empty_query():
    response = client.post("/query", json={"query": ""})
    assert response.status_code == 422  # Pydantic validation


def test_documents_list_endpoint():
    with patch(
        "app.api.routes.documents.list_indexed_filenames",
        return_value=["doc1.pdf", "doc2.txt"],
    ):
        response = client.get("/documents")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert "doc1.pdf" in data["filenames"]


def test_documents_delete_not_found():
    with patch(
        "app.api.routes.documents.delete_document_by_filename", return_value=0
    ):
        response = client.delete("/documents/nonexistent.pdf")
    assert response.status_code == 404
