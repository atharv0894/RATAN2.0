"""
Ingest service — handles document loading, cleaning, chunking, embedding, and storage.
"""
import time
from typing import Any
from app.config.settings import settings
from app.config.logging import get_logger
from app.loaders.loader_factory import load_document
from app.preprocessing.cleaner import clean_text
from app.preprocessing.validator import is_valid_text
from app.chunking.chunker import chunk_document
from app.vectorstore.upsert import upsert_chunks
from app.models.response_models import IngestResponse

logger = get_logger(__name__)


def ingest_file(file_path: str) -> IngestResponse:
    """
    Full ingestion pipeline for a single file.

    Args:
        file_path: Absolute path to the document.

    Returns:
        IngestResponse with chunk count and timing.

    Raises:
        ValueError: For unsupported file types or empty documents.
    """
    t_start = time.perf_counter()
    filename = file_path.split("/")[-1]
    logger.info("Ingestion started | file=%s", filename)

    # 1. Load
    pages_data: list[dict[str, Any]] = load_document(file_path)
    logger.info("Loaded %d pages from %s", len(pages_data), filename)

    # 2. Clean & validate
    valid_pages: list[dict[str, Any]] = []
    for page in pages_data:
        cleaned = clean_text(page["text"])
        if is_valid_text(cleaned):
            page["text"] = cleaned
            valid_pages.append(page)

    if not valid_pages:
        raise ValueError(f"No usable text found in '{filename}'.")

    # 3. Chunk
    chunks = chunk_document(valid_pages)
    logger.info("Chunking complete | chunks=%d", len(chunks))

    # 4. Embed & upsert
    upsert_chunks(chunks)

    elapsed_ms = round((time.perf_counter() - t_start) * 1000, 2)
    logger.info(
        "Ingestion complete | file=%s | chunks=%d | latency=%.1f ms",
        filename, len(chunks), elapsed_ms,
    )
    return IngestResponse(
        message="File ingested successfully.",
        filename=filename,
        chunks_created=len(chunks),
        ingestion_time_ms=elapsed_ms,
    )
