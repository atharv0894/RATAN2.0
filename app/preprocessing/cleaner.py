import re

def clean_text(text: str) -> str:
    """
    Clean the extracted text by removing unnecessary whitespace
    and normalizing line breaks.
    """
    if not text:
        return ""
    
    # Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)
    
    # Normalize line breaks (replace multiple newlines with a single newline)
    text = re.sub(r'[\r\n]+', '\n', text)
    
    return text.strip()
