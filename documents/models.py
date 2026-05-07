import uuid
from django.db import models
from django.conf import settings

class Document(models.Model):
    ACCESS_LEVELS = (('public','Public'),('staff','Staff'),('internal','Internal'))
    STATUS_CHOICES = (('pending','Pending'),('processing','Processing'),('ready','Ready'),('error','Error'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20)   # pdf, txt, image
    file_url = models.CharField(max_length=500)   # Appwrite / local path
    access_level = models.CharField(max_length=10, choices=ACCESS_LEVELS, default='public')
    department = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class DocumentChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    chunk_index = models.IntegerField()
    text = models.TextField()
    embedding_id = models.UUIDField(null=True, blank=True)   # Qdrant point ID
    metadata = models.JSONField(default=dict)                # page, section, etc.
