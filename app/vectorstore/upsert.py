import uuid
from typing import Any, Dict, List
from qdrant_client.models import PointStruct
from app.vectorstore.qdrant_client import get_qdrant_client, COLLECTION_NAME
from app.embeddings.embedding_service import generate_embeddings

def upsert_chunks(chunks: List[Dict[str, Any]]) -> None:
    """
    Generate embeddings for the chunks and store them in Qdrant.
    """
    if not chunks:
        return
        
    client = get_qdrant_client()
    
    # Extract texts to generate embeddings
    texts = [chunk["text"] for chunk in chunks]
    
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = generate_embeddings(texts)
    
    points = []
    for i, chunk in enumerate(chunks):
        # We need a UUID for Qdrant points. We can generate one or use chunk_id if it's a valid UUID.
        # Since we generated a UUID string in the chunker, we'll use it.
        chunk_id = chunk["metadata"]["chunk_id"]
        
        payload = {
            "text": chunk["text"],
            **chunk["metadata"]
        }
        
        points.append(
            PointStruct(
                id=chunk_id,
                vector=embeddings[i],
                payload=payload
            )
        )
        
    print(f"Upserting {len(points)} points into Qdrant...")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print("Upsert complete.")
