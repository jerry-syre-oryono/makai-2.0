import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chats.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'makai.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/chat/<str:conv_id>/", ChatConsumer.as_asgi()),
        ])
    ),
})
