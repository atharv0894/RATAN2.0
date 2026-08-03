"""
Model manager — thin wrapper to surface active provider/model metadata.
"""
from app.llm.provider_factory import ProviderFactory


def get_active_provider_name() -> str:
    """Return the name of the currently configured provider."""
    return ProviderFactory.get_provider().provider_name


def get_active_model_name() -> str:
    """Return the model identifier for the currently configured provider."""
    return ProviderFactory.get_provider().model_name
