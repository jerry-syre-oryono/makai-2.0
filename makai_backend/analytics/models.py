import uuid
from django.db import models
from django.conf import settings

class AIRequestLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    endpoint = models.CharField(max_length=50)
    prompt_tokens = models.IntegerField(default=0)
    completion_tokens = models.IntegerField(default=0)
    latency_ms = models.IntegerField(default=0)
    sources_used = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
