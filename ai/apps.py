from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os


def create_qdrant_collections(sender, **kwargs):
    # This is a safety check that runs after migrations
    from ai.qdrant_client import qdrant
    from qdrant_client.http.models import Distance, VectorParams

    try:
        collections = [c.name for c in qdrant.get_collections().collections]

        if 'makerere_public_docs' not in collections:
            qdrant.create_collection(
                collection_name='makerere_public_docs',
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )

        if 'makerere_internal_docs' not in collections:
            qdrant.create_collection(
                collection_name='makerere_internal_docs',
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
    except Exception:
        # Silently fail during migration signals to avoid blocking deployment
        pass


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'
    path = os.path.dirname(os.path.abspath(__file__))

    def ready(self):
        # Using post_migrate for cleaner separation
        post_migrate.connect(create_qdrant_collections, sender=self)
