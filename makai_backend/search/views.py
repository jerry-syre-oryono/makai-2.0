from rest_framework.views import APIView
from rest_framework.response import Response
from ai.gateway import AIGateway
from users.permissions import IsStaffOrAdmin
from rest_framework.permissions import IsAuthenticated
from ai.throttles import AIRateThrottle

class PublicSearchView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AIRateThrottle]

    def post(self, request):
        query = request.data['query']
        gateway = AIGateway(request.user)
        # The gateway handles role-based filtering internally
        chunks = gateway.retrieve_context(query)
        return Response({'results': chunks})

class InternalSearchView(APIView):
    permission_classes = [IsStaffOrAdmin]
    throttle_classes = [AIRateThrottle]

    def post(self, request):
        query = request.data['query']
        gateway = AIGateway(request.user)
        chunks = gateway.retrieve_context(query)
        return Response({'results': chunks})
