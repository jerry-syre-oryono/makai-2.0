from django.apps import AppConfig
import os


class AgentsConfig(AppConfig):
    name = 'agents'
    path = os.path.dirname(os.path.abspath(__file__))
