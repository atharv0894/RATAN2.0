"""
Updated chunker.py — chunk size / overlap driven by Settings.
"""
import uuid
from typing import Any
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import settings


def chunk_document(
    pages_data: list[dict[str, Any]],
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> list[dict[str, Any]]:
    """
    Split document pages into smaller, overlapping chunks.
    Chunk size and overlap default to values from Settings.
    """
    chunk_size = chunk_size or settings.chunk_size
    chunk_overlap = chunk_overlap or settings.chunk_overlap

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunks: list[dict[str, Any]] = []
    for page in pages_data:
        for text in splitter.split_text(page["text"]):
            meta = page["metadata"].copy()
            meta["chunk_id"] = str(uuid.uuid4())
            chunks.append({"text": text, "metadata": meta})

    return chunks
