from typing import Any, Dict, List
from app.utils.file_utils import get_file_name

def load_txt(file_path: str) -> List[Dict[str, Any]]:
    """
    Load a text file and extract its content.
    Returns a list containing a single dictionary with the text and metadata.
    """
    filename = get_file_name(file_path)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    return [{
        "text": text,
        "metadata": {
            "filename": filename,
            "page_number": 1  # TXT files don't have pages, default to 1
        }
    }]
