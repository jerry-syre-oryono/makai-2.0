from django.urls import path
from .views import PublicSearchView, InternalSearchView

urlpatterns = [
    path('public/', PublicSearchView.as_view(), name='public_search'),
    path('internal/', InternalSearchView.as_view(), name='internal_search'),
]
