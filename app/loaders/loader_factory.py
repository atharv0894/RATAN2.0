from typing import Any, Dict, List
from app.loaders.pdf_loader import load_pdf
from app.loaders.txt_loader import load_txt
from app.utils.file_utils import get_file_extension

def load_document(file_path: str) -> List[Dict[str, Any]]:
    """
    Factory function to load a document based on its extension.
    Returns a list of dictionaries with 'text' and 'metadata'.
    """
    ext = get_file_extension(file_path)
    
    if ext == '.pdf':
        return load_pdf(file_path)
    elif ext == '.txt':
        return load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
