"""
Groq LLM provider implementation.
"""
import groq

from app.config.settings import settings
from app.config.logging import get_logger
from app.llm.base_provider import BaseLLMProvider

logger = get_logger(__name__)


class GroqProvider(BaseLLMProvider):
    """LLM provider backed by the Groq API."""

    def __init__(self) -> None:
        api_key = settings.groq_api_key
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in environment variables.")
        self._client = groq.Groq(api_key=api_key)
        self._model = settings.groq_model

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def provider_name(self) -> str:
        return "groq"

    @property
    def model_name(self) -> str:
        return self._model

    # ------------------------------------------------------------------
    # Core
    # ------------------------------------------------------------------

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Send the prompt to Groq and return the generated text."""
        logger.info("Calling Groq API | model=%s", self._model)
        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                max_tokens=1024,
            )
            return completion.choices[0].message.content.strip()
        except groq.AuthenticationError:
            raise ValueError("Invalid Groq API key.")
        except groq.NotFoundError:
            raise ValueError(f"Groq model '{self._model}' not found.")
        except groq.RateLimitError:
            raise RuntimeError("Groq rate limit exceeded. Please retry later.")
        except groq.APIConnectionError as exc:
            raise RuntimeError(f"Groq connection error: {exc}") from exc
        except groq.APIError as exc:
            raise RuntimeError(f"Groq API error: {exc}") from exc
