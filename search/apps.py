from django.apps import AppConfig
import os


class SearchConfig(AppConfig):
    name = 'search'
    path = os.path.dirname(os.path.abspath(__file__))
