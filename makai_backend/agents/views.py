from rest_framework.views import APIView
from rest_framework.response import Response
from documents.models import Document
from .summarizer import summarize_document
from users.permissions import IsStaffOrAdmin

class DocumentSummaryView(APIView):
    permission_classes = [IsStaffOrAdmin]
    def post(self, request):
        doc_id = request.data['document_id']
        doc = Document.objects.get(id=doc_id)
        # Gather all chunk texts
        chunks = doc.chunks.order_by('chunk_index')
        full_text = "\n".join([c.text for c in chunks])
        summary = summarize_document(full_text)
        return Response({'summary': summary})
