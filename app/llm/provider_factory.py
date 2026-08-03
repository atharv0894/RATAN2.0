"""
Provider factory — Groq only (Ollama removed per project requirements).
"""
from app.config.settings import settings
from app.config.logging import get_logger
from app.llm.base_provider import BaseLLMProvider

logger = get_logger(__name__)

_provider_cache: BaseLLMProvider | None = None


class ProviderFactory:
    """Instantiates and caches the configured LLM provider."""

    @classmethod
    def get_provider(cls) -> BaseLLMProvider:
        """Return a cached provider. Only 'groq' is supported."""
        global _provider_cache
        if _provider_cache is not None:
            return _provider_cache

        provider_name = settings.llm_provider.lower()
        logger.info("Initialising LLM provider: %s", provider_name)

        if provider_name == "groq":
            from app.llm.groq_client import GroqProvider
            _provider_cache = GroqProvider()
        else:
            raise ValueError(
                f"Unsupported LLM_PROVIDER '{provider_name}'. "
                "Only 'groq' is supported."
            )

        return _provider_cache
