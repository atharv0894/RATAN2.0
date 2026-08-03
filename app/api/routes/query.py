"""
FastAPI route — POST /query
"""
from fastapi import APIRouter, HTTPException, status
from app.config.logging import get_logger
from app.services.query_service import handle_query
from app.models.request_models import QueryRequest
from app.models.response_models import RAGResponse

router = APIRouter(prefix="/query", tags=["Query"])
logger = get_logger(__name__)


@router.post("", response_model=RAGResponse)
async def query_documents(request: QueryRequest) -> RAGResponse:
    """
    Run the RAG pipeline for a natural language query.

    - **query**: The user's question.
    - **top_k**: How many chunks to retrieve (1–20, default 5).
    """
    try:
        return handle_query(request.query, top_k=request.top_k)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except RuntimeError as exc:
        logger.exception("LLM generation failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        )
    except Exception as exc:
        logger.exception("Unexpected query error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query failed: {exc}",
        )
