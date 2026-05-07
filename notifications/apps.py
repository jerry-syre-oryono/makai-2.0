from django.apps import AppConfig
import os


class NotificationsConfig(AppConfig):
    name = 'notifications'
    path = os.path.dirname(os.path.abspath(__file__))
