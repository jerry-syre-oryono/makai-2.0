from django.apps import AppConfig
import os


class DocumentsConfig(AppConfig):
    name = 'documents'
    path = os.path.dirname(os.path.abspath(__file__))
