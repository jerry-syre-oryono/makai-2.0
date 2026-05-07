from django.urls import path
from .views import DocumentSummaryView

urlpatterns = [
    path('summarize/', DocumentSummaryView.as_view(), name='summarize_document'),
]
