"""
RAG pipeline orchestrator.

Flow:
    query → retrieve (top_k) → trim (max_context_chunks) → build prompt
          → LLM generate → parse → RAGResponse
"""
import time
from app.config.settings import settings
from app.config.logging import get_logger
from app.vectorstore.search import search_vectors
from app.prompt.system_prompt import SYSTEM_PROMPT
from app.prompt.rag_prompt import build_rag_prompt
from app.llm.provider_factory import ProviderFactory
from app.llm.response_parser import parse_response
from app.models.response_models import RAGResponse, RetrievedChunk, Source

logger = get_logger(__name__)


def run_rag_pipeline(query: str, top_k: int | None = None) -> RAGResponse:
    """
    Execute the full RAG pipeline and return a structured RAGResponse.

    Args:
        query:  User question string.
        top_k:  Number of chunks to retrieve (defaults to settings.top_k).

    Returns:
        RAGResponse with answer, sources, chunks, model metadata and latency.
    """
    top_k = top_k or settings.top_k
    t_start = time.perf_counter()

    # ── 1. Retrieve ─────────────────────────────────────────────────────
    logger.info("Retrieval started | top_k=%d", top_k)
    t_ret = time.perf_counter()
    raw_results = search_vectors(query, top_k=top_k)
    ret_ms = (time.perf_counter() - t_ret) * 1000
    logger.info("Retrieval complete | docs=%d | latency=%.1f ms", len(raw_results), ret_ms)

    if not raw_results:
        provider = ProviderFactory.get_provider()
        return RAGResponse(
            answer="I don't know.",
            sources=[],
            retrieved_chunks=[],
            model=provider.model_name,
            provider=provider.provider_name,
            latency_ms=round((time.perf_counter() - t_start) * 1000, 2),
        )

    # ── 2. Convert to typed chunks ───────────────────────────────────────
    retrieved_chunks: list[RetrievedChunk] = [
        RetrievedChunk(
            text=r.get("text", ""),
            score=r.get("similarity_score", 0.0),
            filename=r.get("filename", "unknown"),
            page_number=r.get("page_number", 0),
            chunk_id=str(r.get("chunk_id", "")),
        )
        for r in raw_results
    ]

    # ── 3. Trim to max_context_chunks (token budget) ─────────────────────
    context_chunks = retrieved_chunks[: settings.max_context_chunks]

    # ── 4. Build prompt ──────────────────────────────────────────────────
    user_prompt = build_rag_prompt(query, context_chunks)

    # ── 5. Generate ──────────────────────────────────────────────────────
    provider = ProviderFactory.get_provider()
    logger.info(
        "Generation started | provider=%s | model=%s",
        provider.provider_name, provider.model_name
    )
    t_gen = time.perf_counter()
    raw_answer = provider.generate(SYSTEM_PROMPT, user_prompt)
    gen_ms = (time.perf_counter() - t_gen) * 1000
    logger.info("Generation complete | latency=%.1f ms", gen_ms)

    answer = parse_response(raw_answer)

    # ── 6. Build citations ───────────────────────────────────────────────
    sources: list[Source] = [
        Source(
            filename=c.filename,
            page_number=c.page_number,
            chunk_id=c.chunk_id,
        )
        for c in context_chunks
    ]

    total_ms = round((time.perf_counter() - t_start) * 1000, 2)
    logger.info("Pipeline complete | total_latency=%.1f ms", total_ms)

    return RAGResponse(
        answer=answer,
        sources=sources,
        retrieved_chunks=retrieved_chunks,
        model=provider.model_name,
        provider=provider.provider_name,
        latency_ms=total_ms,
    )
