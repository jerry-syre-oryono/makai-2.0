import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue

qdrant = QdrantClient(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_API_KEY'),
)

def init_collections():
    # Public collection
    collections = qdrant.get_collections().collections
    if not any(c.name == 'makerere_public_docs' for c in collections):
        qdrant.create_collection(
            collection_name='makerere_public_docs',
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
    if not any(c.name == 'makerere_internal_docs' for c in collections):
        qdrant.create_collection(
            collection_name='makerere_internal_docs',
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
