"""
FastAPI route — POST /ingest
Accepts multipart file upload, writes to a temp file, runs ingest pipeline.
"""
import os
import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.config.constants import SUPPORTED_EXTENSIONS
from app.config.logging import get_logger
from app.services.ingest_service import ingest_file
from app.models.response_models import IngestResponse

router = APIRouter(prefix="/ingest", tags=["Ingestion"])
logger = get_logger(__name__)


@router.post("", response_model=IngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(file: UploadFile = File(...)) -> IngestResponse:
    """
    Upload a document (PDF or TXT), chunk it, embed it, and store in Qdrant.

    - **file**: multipart/form-data file upload.
    """
    filename = file.filename or "upload"
    ext = os.path.splitext(filename)[1].lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{ext}'. Supported: {SUPPORTED_EXTENSIONS}",
        )

    # Write upload to a temp file so existing loaders can read it by path
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        result = ingest_file(tmp_path)
        # Use the original uploaded filename in the response
        result.filename = filename
        return result
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))
    except Exception as exc:
        logger.exception("Ingest failed for file=%s", filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {exc}",
        )
    finally:
        os.unlink(tmp_path)
