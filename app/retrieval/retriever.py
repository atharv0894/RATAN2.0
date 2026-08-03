from typing import Any, Dict, List
from app.vectorstore.search import search_vectors

def retrieve_top_k(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve the top-K most relevant chunks for a given query.
    Delegates to the vector store search function.
    """
    print(f"Retrieving top {top_k} chunks for query: '{query}'")
    results = search_vectors(query, top_k=top_k)
    return results

def format_retrieval_results(results: List[Dict[str, Any]]) -> None:
    """
    Display the retrieved chunks with their metadata.
    """
    print(f"\n--- Retrieved {len(results)} Chunks ---")
    for i, result in enumerate(results, 1):
        print(f"\n[Result {i}]")
        print(f"Similarity Score: {result.get('similarity_score', 0):.4f}")
        print(f"Filename: {result.get('filename', 'Unknown')}")
        print(f"Page Number: {result.get('page_number', 'N/A')}")
        print(f"Chunk ID: {result.get('chunk_id', 'N/A')}")
        print("-" * 20)
        # We cap text printing to avoid huge outputs, but display enough context.
        text = result.get('text', '')
        print(f"Text:\n{text}")
        print("-" * 40)
