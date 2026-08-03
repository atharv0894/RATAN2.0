"""
FastAPI dependency injection helpers.
"""
from app.config.settings import settings


def get_settings():
    """Yield the global settings instance."""
    return settings
