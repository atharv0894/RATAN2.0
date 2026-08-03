"""
RAG prompt builder — assembles context + question into a user-turn prompt.

Keeps prompt construction fully independent of any LLM implementation.
"""
from app.config.settings import settings
from app.prompt.citation_prompt import CITATION_INSTRUCTION
from app.models.response_models import RetrievedChunk


def build_rag_prompt(query: str, chunks: list[RetrievedChunk]) -> str:
    """
    Build a context-grounded user prompt.

    Args:
        query:  The user's question.
        chunks: Retrieved chunks (already trimmed to max_context_chunks).

    Returns:
        Formatted prompt string ready to pass to an LLM.

    Raises:
        ValueError: If query is empty or no chunks are provided.
    """
    if not query.strip():
        raise ValueError("Query must not be empty.")
    if not chunks:
        raise ValueError("No context chunks provided to build prompt.")

    context_parts: list[str] = []
    total_len = 0

    for chunk in chunks:
        entry = (
            f"[File: {chunk.filename} | Page: {chunk.page_number}]\n"
            f"{chunk.text}"
        )
        if total_len + len(entry) > settings.max_context_length:
            break
        context_parts.append(entry)
        total_len += len(entry)

    context_str = "\n\n---\n\n".join(context_parts)

    prompt = (
        f"Context:\n{context_str}"
        f"{CITATION_INSTRUCTION}"
        f"\n\nQuestion:\n{query}"
    )
    return prompt
