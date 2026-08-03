"""
Updated embedding_service.py — uses the new get_embedding_model() helper.
"""
from app.embeddings.embedding_model import get_embedding_model


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """Generate embeddings for a list of texts."""
    model = get_embedding_model()
    return model.encode(texts).tolist()


def generate_embedding(text: str) -> list[float]:
    """Generate an embedding for a single text."""
    model = get_embedding_model()
    return model.encode(text).tolist()
