"""
Answer generator — thin shim that delegates to run_rag_pipeline.
Kept for backward-compatibility and for direct CLI use.
"""
from app.rag.rag_pipeline import run_rag_pipeline
from app.models.response_models import RAGResponse


def generate_answer(query: str, top_k: int = 5) -> RAGResponse:
    """
    Generate a grounded answer for the given query.

    Args:
        query:  User question.
        top_k:  Chunks to retrieve.

    Returns:
        Structured RAGResponse.
    """
    return run_rag_pipeline(query, top_k=top_k)
