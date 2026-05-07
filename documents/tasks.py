from celery import shared_task
from django.core.files.storage import default_storage
import os
import uuid
from PyPDF2 import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from ai.embeddings import get_embedding
from ai.qdrant_client import qdrant
from .models import Document, DocumentChunk

@shared_task
def process_document(doc_id):
    doc = Document.objects.get(id=doc_id)
    doc.status = 'processing'
    doc.save()

    try:
        # 1. Extract text from file
        file_path = default_storage.path(doc.file_url)
        text = ""
        if doc.file_type.lower() == 'pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text()
        elif doc.file_type.lower() in ['png', 'jpg', 'jpeg']:
            # Initialize OCR only when needed
            try:
                from paddleocr import PaddleOCR
                ocr_engine = PaddleOCR(use_angle_cls=True, lang='en')
                result = ocr_engine.ocr(file_path, cls=True)
                for line in result[0]:
                    text += line[1][0] + " "
            except ImportError:
                raise Exception("OCR engine (PaddleOCR) not available.")
        else:  # txt
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

        # 2. Chunk text
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_text(text)

        # 3. Embed and store in Qdrant
        collection = 'makerere_internal_docs' if doc.access_level in ['staff','internal'] else 'makerere_public_docs'
        for idx, chunk_text in enumerate(chunks):
            embedding = get_embedding(chunk_text)
            point_id = str(uuid.uuid4())
            qdrant.upsert(
                collection_name=collection,
                points=[{
                    'id': point_id,
                    'vector': embedding,
                    'payload': {
                        'text': chunk_text,
                        'document_id': str(doc.id),
                        'access_level': doc.access_level,
                        'department': doc.department,
                        'chunk_index': idx,
                    }
                }]
            )
            DocumentChunk.objects.create(
                document=doc,
                chunk_index=idx,
                text=chunk_text,
                embedding_id=point_id,
                metadata={'page': idx//10 + 1}  # dummy
            )
        doc.status = 'ready'
        doc.save()
    except Exception as e:
        doc.status = 'error'
        doc.save()
        raise e
