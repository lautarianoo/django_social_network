import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.core import serializers
from .models import Notification
from .serializers import NotificationSerializer

User = get_user_model()


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    @database_sync_to_async
    def fetch_messages(self):
        user = self.scope['user']
        notifications = Notification.objects.select_related('author').filter(reciever=user, deleted=False, read=False)[:6]
        serializer = NotificationSerializer(notifications, many=True)
        content = {
            'command': 'notifications',
            'notifications': json.dumps(serializer.data)
        }
        self.send_json(content)

    async def connect(self):
        user = self.scope['user']
        grp = "new_comment_notifications_{}".format(user.username)
        await self.accept()
        await self.channel_layer.group_add(grp, self.channel_name)

    async def disconnect(self, code):
        user = self.scope['user']
        grp = "new_comment_notifications_{}".format(user.username)
        await self.channel_layer.group_discard(grp, self.channel_name)

    async def notify(self, event):
        await self.send_json(event)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        data = json.loads(text_data)
        if data['command'] == 'fetch_notifications':
            await self.fetch_messages()

