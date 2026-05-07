from django.core.management.base import BaseCommand
from ai.qdrant_client import qdrant
from qdrant_client.http.models import Distance, VectorParams

class Command(BaseCommand):
    help = 'Initialize Qdrant collections if they do not exist'

    def handle(self, *args, **options):
        try:
            collections = [c.name for c in qdrant.get_collections().collections]

            if 'makerere_public_docs' not in collections:
                qdrant.create_collection(
                    collection_name='makerere_public_docs',
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
                self.stdout.write(self.style.SUCCESS('Created public collection.'))
            else:
                self.stdout.write('Public collection already exists.')

            if 'makerere_internal_docs' not in collections:
                qdrant.create_collection(
                    collection_name='makerere_internal_docs',
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
                self.stdout.write(self.style.SUCCESS('Created internal collection.'))
            else:
                self.stdout.write('Internal collection already exists.')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error initializing Qdrant: {str(e)}'))
