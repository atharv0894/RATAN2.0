"""
Tests for the LLM provider abstraction and factory.
"""
import pytest
from unittest.mock import patch, MagicMock
from app.llm.base_provider import BaseLLMProvider


def test_base_provider_is_abstract():
    """BaseLLMProvider cannot be instantiated directly."""
    with pytest.raises(TypeError):
        BaseLLMProvider()


def test_provider_factory_groq(monkeypatch):
    """ProviderFactory returns a GroqProvider when LLM_PROVIDER=groq."""
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "test-key")

    # Reset cache
    import app.llm.provider_factory as pf
    pf._provider_cache = None

    with patch("app.llm.groq_client.groq.Groq"):
        from app.llm.provider_factory import ProviderFactory
        provider = ProviderFactory.get_provider()
        assert provider.provider_name == "groq"

    pf._provider_cache = None  # cleanup


def test_provider_factory_unknown_raises(monkeypatch):
    """ProviderFactory raises for unsupported providers."""
    monkeypatch.setenv("LLM_PROVIDER", "unknown_provider")

    import app.llm.provider_factory as pf
    pf._provider_cache = None

    # Force settings reload
    with patch("app.llm.provider_factory.settings") as mock_settings:
        mock_settings.llm_provider = "unknown_provider"
        from app.llm.provider_factory import ProviderFactory
        with pytest.raises(ValueError, match="Unsupported LLM_PROVIDER"):
            ProviderFactory.get_provider()

    pf._provider_cache = None
