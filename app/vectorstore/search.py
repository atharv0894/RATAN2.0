from typing import Any, Dict, List
from app.vectorstore.qdrant_client import get_qdrant_client, COLLECTION_NAME
from app.embeddings.embedding_service import generate_embedding


def search_vectors(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for the most similar chunks in Qdrant based on the query.
    Uses query_points() (qdrant-client >= 1.9 API).
    Returns the payload of the top_k matching chunks along with their similarity score.
    """
    client = get_qdrant_client()
    query_vector = generate_embedding(query)

    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    )

    results = []
    for point in result.points:
        item = point.payload.copy() if point.payload else {}
        item["similarity_score"] = point.score
        item["chunk_id"] = str(point.id)
        results.append(item)

    return results
