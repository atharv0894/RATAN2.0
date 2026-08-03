"""
Application-wide constants that never change at runtime.
"""

SUPPORTED_EXTENSIONS: list[str] = [".pdf", ".txt"]

LLM_PROVIDER_GROQ = "groq"
LLM_PROVIDER_OLLAMA = "ollama"
SUPPORTED_LLM_PROVIDERS = {LLM_PROVIDER_GROQ, LLM_PROVIDER_OLLAMA}
