def is_valid_text(text: str) -> bool:
    """
    Validate if the extracted text is meaningful.
    Returns False if text is empty or too short.
    """
    if not text:
        return False
        
    # Check if text is just whitespace or too short to be useful
    if len(text.strip()) < 10:
        return False
        
    return True
