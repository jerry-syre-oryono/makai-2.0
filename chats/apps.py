from django.apps import AppConfig
import os


class ChatsConfig(AppConfig):
    name = 'chats'
    path = os.path.dirname(os.path.abspath(__file__))
