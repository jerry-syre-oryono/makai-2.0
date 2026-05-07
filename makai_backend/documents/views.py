from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
from .models import Document
from .tasks import process_document
from users.permissions import IsStaffOrAdmin

class UploadDocumentView(APIView):
    permission_classes = [IsStaffOrAdmin]
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES['file']
        # Save locally
        file_path = default_storage.save(f"uploads/{file.name}", file)
        doc = Document.objects.create(
            uploader=request.user,
            title=request.data.get('title', file.name),
            file_type=file.name.split('.')[-1],
            file_url=file_path,
            access_level=request.data.get('access_level', 'staff'),
            department=request.data.get('department'),
            status='pending'
        )
        process_document.delay(str(doc.id))
        return Response({'id': doc.id, 'status': 'pending'})
