"""
Document service — list and delete indexed documents in Qdrant.
"""
from app.config.settings import settings
from app.config.logging import get_logger
from app.vectorstore.qdrant_client import get_qdrant_client
from qdrant_client.models import Filter, FieldCondition, MatchValue

logger = get_logger(__name__)


def list_indexed_filenames() -> list[str]:
    """
    Return the unique filenames of all indexed documents.
    Scrolls through all Qdrant points to collect distinct filenames.
    """
    client = get_qdrant_client()
    filenames: set[str] = set()
    offset = None

    while True:
        records, offset = client.scroll(
            collection_name=settings.collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False,
        )
        for r in records:
            if r.payload and "filename" in r.payload:
                filenames.add(r.payload["filename"])
        if offset is None:
            break

    return sorted(filenames)


def delete_document_by_filename(filename: str) -> int:
    """
    Delete all chunks whose 'filename' payload matches the given name.

    Returns:
        Number of points deleted.
    """
    client = get_qdrant_client()

    # Collect IDs for the target filename
    ids_to_delete: list[str] = []
    offset = None

    while True:
        records, offset = client.scroll(
            collection_name=settings.collection_name,
            scroll_filter=Filter(
                must=[FieldCondition(key="filename", match=MatchValue(value=filename))]
            ),
            limit=100,
            offset=offset,
            with_payload=False,
            with_vectors=False,
        )
        ids_to_delete.extend(str(r.id) for r in records)
        if offset is None:
            break

    if ids_to_delete:
        client.delete(
            collection_name=settings.collection_name,
            points_selector=ids_to_delete,
        )
        logger.info("Deleted %d chunks for file=%s", len(ids_to_delete), filename)

    return len(ids_to_delete)
