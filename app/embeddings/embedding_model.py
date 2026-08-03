"""
Updated embedding_model.py — model name driven by Settings.
"""
from sentence_transformers import SentenceTransformer
from app.config.settings import settings
from app.config.logging import get_logger

logger = get_logger(__name__)

_model: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Return the lazily-loaded singleton embedding model."""
    global _model
    if _model is None:
        logger.info("Loading embedding model: %s", settings.embedding_model)
        _model = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded.")
    return _model
