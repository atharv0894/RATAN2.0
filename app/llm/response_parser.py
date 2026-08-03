"""
Response parser — normalises raw LLM output.
"""


def parse_response(raw: str) -> str:
    """
    Strip leading/trailing whitespace from a raw LLM response.
    Extend this function for structured output parsing in the future.
    """
    return raw.strip() if raw else "I don't know."
