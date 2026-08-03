"""
FastAPI route — GET /health
"""
from fastapi import APIRouter
from app.config.settings import settings
from app.config.logging import get_logger
from app.models.response_models import HealthResponse
from app.vectorstore.qdrant_client import get_qdrant_client
from app.llm.provider_factory import ProviderFactory

router = APIRouter(prefix="/health", tags=["Health"])
logger = get_logger(__name__)


@router.get("", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Return the operational status of the backend and its dependencies."""
    # Check Qdrant
    qdrant_status = "ok"
    try:
        client = get_qdrant_client()
        client.get_collections()
    except Exception as exc:
        qdrant_status = f"error: {exc}"

    # Resolve active provider metadata (don't call generate to avoid cost)
    try:
        provider = ProviderFactory.get_provider()
        provider_name = provider.provider_name
        model_name = provider.model_name
    except Exception as exc:
        provider_name = "error"
        model_name = str(exc)

    return HealthResponse(
        status="ok",
        provider=provider_name,
        model=model_name,
        qdrant=qdrant_status,
        details={
            "collection": settings.collection_name,
            "embedding_model": settings.embedding_model,
            "top_k": settings.top_k,
            "max_context_chunks": settings.max_context_chunks,
        },
    )
