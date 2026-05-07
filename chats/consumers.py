import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from ai.gateway import AIGateway
from ai.embeddings import get_embedding

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conv_id']
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_msg = data['message']
        # Save user message
        conversation = await self.get_conversation()
        await self.save_message(conversation, 'user', user_msg)

        # RAG retrieval
        gateway = AIGateway(self.user, self.conversation_id)
        # We call the sync methods in a thread to avoid blocking the event loop
        chunks = await database_sync_to_async(gateway.retrieve_context)(user_msg)
        # Stream assistant response
        full_response = ""
        def get_response():
            return gateway.stream_response(user_msg, chunks)
        
        # Iterating over sync generator in async
        for chunk in await database_sync_to_async(list)(get_response()):
            full_response += chunk
            await self.send(text_data=json.dumps({'type': 'chunk', 'content': chunk}))
        # Save assistant message
        await self.save_message(conversation, 'model', full_response, chunks)
        await self.send(text_data=json.dumps({'type': 'done', 'sources': chunks}))

    @database_sync_to_async
    def get_conversation(self):
        conv, _ = Conversation.objects.get_or_create(id=self.conversation_id, user=self.user)
        return conv

    @database_sync_to_async
    def save_message(self, conv, role, content, sources=None):
        return Message.objects.create(
            conversation=conv,
            role=role,
            content=content,
            sources=sources or []
        )
