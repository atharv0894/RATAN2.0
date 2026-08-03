"""
Query service — entry point for the full RAG query flow.
"""
from app.config.logging import get_logger
from app.rag.rag_pipeline import run_rag_pipeline
from app.models.response_models import RAGResponse

logger = get_logger(__name__)


def handle_query(query: str, top_k: int = 5) -> RAGResponse:
    """
    Execute the RAG pipeline for a user query.

    Args:
        query:  User's natural language question.
        top_k:  Number of chunks to retrieve.

    Returns:
        Structured RAGResponse.
    """
    logger.info("Query received | query=%s | top_k=%d", query[:80], top_k)
    return run_rag_pipeline(query, top_k=top_k)
