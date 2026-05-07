from django.urls import path
from .views import UsageStatsView

urlpatterns = [
    path('stats/', UsageStatsView.as_view(), name='usage_stats'),
]
