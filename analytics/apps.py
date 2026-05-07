from django.apps import AppConfig
import os


class AnalyticsConfig(AppConfig):
    name = 'analytics'
    path = os.path.dirname(os.path.abspath(__file__))
