"""
LLM provider abstraction.

All concrete providers must implement this interface.
The retrieval and prompt layers NEVER import a concrete provider directly.
"""
from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Send a prompt to the LLM and return the raw text response.

        Args:
            system_prompt: Instructions for the model's behaviour.
            user_prompt:   The actual user-facing prompt (context + question).

        Returns:
            Generated text string.
        """
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier (e.g. 'groq', 'ollama')."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Model identifier used for this provider."""
        ...
