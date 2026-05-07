from rest_framework.views import APIView
from rest_framework.response import Response
from users.permissions import IsAdmin
from .models import AIRequestLog
from django.db.models import Count, Sum
from chats.models import Message

class UsageStatsView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        total_requests = AIRequestLog.objects.count()
        
        # Calculate total tokens safely
        stats = AIRequestLog.objects.aggregate(
            prompt=Sum('prompt_tokens'),
            completion=Sum('completion_tokens')
        )
        total_tokens = (stats['prompt'] or 0) + (stats['completion'] or 0)
        
        # top 10 queries (simplified – from Message content)
        top_queries = Message.objects.filter(role='user').values('content').annotate(count=Count('id')).order_by('-count')[:10]
        
        return Response({
            'total_requests': total_requests,
            'total_tokens': total_tokens,
            'top_queries': list(top_queries)
        })
