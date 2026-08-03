"""
FastAPI routes — GET /documents, DELETE /documents/{filename}
"""
from fastapi import APIRouter, HTTPException, status
from app.config.logging import get_logger
from app.services.document_service import list_indexed_filenames, delete_document_by_filename
from app.models.response_models import DocumentListResponse

router = APIRouter(prefix="/documents", tags=["Documents"])
logger = get_logger(__name__)


@router.get("", response_model=DocumentListResponse)
async def list_documents() -> DocumentListResponse:
    """Return all unique filenames indexed in Qdrant."""
    try:
        filenames = list_indexed_filenames()
        return DocumentListResponse(total=len(filenames), filenames=filenames)
    except Exception as exc:
        logger.exception("Failed to list documents")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not list documents: {exc}",
        )


@router.delete("/{filename}", status_code=status.HTTP_200_OK)
async def delete_document(filename: str) -> dict:
    """
    Delete all indexed chunks for the given filename.

    - **filename**: The exact filename as stored during ingestion (e.g. `report.pdf`).
    """
    try:
        deleted = delete_document_by_filename(filename)
        if deleted == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No indexed chunks found for filename='{filename}'.",
            )
        return {"message": f"Deleted {deleted} chunks for '{filename}'."}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Failed to delete document=%s", filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deletion failed: {exc}",
        )
