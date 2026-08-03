"""
Updated vectorstore/qdrant_client.py — driven by Settings.
"""
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.config.settings import settings
from app.config.logging import get_logger

logger = get_logger(__name__)

_qdrant_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    """Return a lazily-initialised Qdrant client singleton."""
    global _qdrant_client
    if _qdrant_client is not None:
        return _qdrant_client

    if settings.qdrant_use_local:
        os.makedirs(settings.qdrant_path, exist_ok=True)
        logger.info("Connecting to local Qdrant at path=%s", settings.qdrant_path)
        _qdrant_client = QdrantClient(path=settings.qdrant_path)
    else:
        logger.info(
            "Connecting to Qdrant server at %s:%s",
            settings.qdrant_host, settings.qdrant_port
        )
        _qdrant_client = QdrantClient(
            host=settings.qdrant_host, port=settings.qdrant_port
        )

    _ensure_collection(_qdrant_client)
    return _qdrant_client


def _ensure_collection(client: QdrantClient) -> None:
    """Create the Qdrant collection if it does not already exist."""
    if not client.collection_exists(settings.collection_name):
        logger.info("Creating Qdrant collection: %s", settings.collection_name)
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(
                size=settings.vector_size,
                distance=Distance.COSINE,
            ),
        )


# Keep backward-compatible alias used in existing vectorstore modules
COLLECTION_NAME = settings.collection_name
