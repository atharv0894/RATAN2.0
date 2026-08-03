from typing import Any, Dict, List
from pypdf import PdfReader
from app.utils.file_utils import get_file_name

def load_pdf(file_path: str) -> List[Dict[str, Any]]:
    """
    Load a PDF file and extract text page by page.
    Returns a list of dictionaries containing the text and metadata for each page.
    """
    reader = PdfReader(file_path)
    filename = get_file_name(file_path)
    pages_data = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages_data.append({
                "text": text,
                "metadata": {
                    "filename": filename,
                    "page_number": i + 1
                }
            })
    return pages_data
