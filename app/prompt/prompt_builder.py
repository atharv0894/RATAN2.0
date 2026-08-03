from typing import List, Dict, Any
from app.prompt.templates import USER_PROMPT_TEMPLATE

def build_prompt(query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    """
    Combines the retrieved chunks and user question into a structured prompt.
    """
    if not retrieved_chunks:
        return ""

    context_texts = []
    for chunk in retrieved_chunks:
        text = chunk.get('text', '').strip()
        if text:
            context_texts.append(f"- {text}")
            
    context_str = "\n".join(context_texts)
    
    return USER_PROMPT_TEMPLATE.format(context=context_str, question=query)
