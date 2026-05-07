from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API schema & docs — publicly accessible
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema', permission_classes=[AllowAny]), name='redoc'),

    # App routes
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/documents/', include('documents.urls')),
    path('api/v1/search/', include('search.urls')),
    path('api/v1/agents/', include('agents.urls')),
    path('api/v1/analytics/', include('analytics.urls')),
]
