from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('users.urls')),
    path('api/v1/documents/', include('documents.urls')),
    path('api/v1/search/', include('search.urls')),
    path('api/v1/agents/', include('agents.urls')),
    path('api/v1/analytics/', include('analytics.urls')),
]
