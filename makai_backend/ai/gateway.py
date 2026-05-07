import google.generativeai as genai
from .qdrant_client import qdrant
from .embeddings import get_embedding
from django.conf import settings
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('models/gemini-1.5-flash')

class AIGateway:
    def __init__(self, user, conversation_id=None):
        self.user = user
        self.conversation_id = conversation_id
        self.history = []  # list of dicts {"role":"user/model","parts":[...]}

    def _get_access_level_filter(self):
        from qdrant_client.http.models import Filter, FieldCondition, MatchValue
        if self.user.role == 'admin':
            return None   # no filter = all docs
        if self.user.role == 'staff':
            return Filter(
                must=[FieldCondition(key='access_level', match=MatchValue(value='staff'))]
            )
        # student
        return Filter(
            must=[FieldCondition(key='access_level', match=MatchValue(value='public'))]
        )

    def retrieve_context(self, query: str, top_k: int = 5):
        query_emb = get_embedding(query)
        collection = 'makerere_public_docs' if self.user.role == 'student' else 'makerere_internal_docs'
        filter_cond = self._get_access_level_filter()
        results = qdrant.search(
            collection_name=collection,
            query_vector=query_emb,
            limit=top_k,
            query_filter=filter_cond,
            with_payload=True,
        )
        chunks = []
        for hit in results:
            chunks.append({
                'text': hit.payload['text'],
                'document_id': hit.payload['document_id'],
                'score': hit.score,
            })
        return chunks

    def stream_response(self, user_message: str, chunks: list):
        context_str = "\n\n".join([f"[{i+1}] {c['text']}" for i, c in enumerate(chunks)])
        prompt = f"""You are MAKAI, the intelligent assistant of Makerere University.
Use the following pieces of context to answer the user's question.
If you don't know, just say so.

Context:
{context_str}

User: {user_message}
Assistant:"""
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            yield chunk.text
