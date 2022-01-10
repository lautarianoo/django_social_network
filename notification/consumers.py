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
