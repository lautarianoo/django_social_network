import json
from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from .models import Message, Room
User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None

    def new_message(self, data):

        author = data['author']
        author_user = User.objects.filter(username=author.username)[0]
        message = Message.objects.create(
            author=author_user,
            text=data['message'],
            room=self.room
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def typing_start(self, data):
        author = data['author']
        content = {
            'command': 'typing_start',
            'message': author
        }
        return self.send_chat_message(content)

    def typing_stop(self, data):
        content = {
            'command': 'typing_stop'
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    @staticmethod
    def message_to_json(message):
        return {
            'author': message.author.username,
            'content': message.text,
            'timestamp': str(message.date_add)
        }

    commands = {
        'new_message': new_message,
        'typing_start': typing_start,
        'typing_stop': typing_stop,
    }

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_id = f'chat_{self.room_id}'
        self.user = self.scope['user']
        self.room = Room.objects.filter(id=self.room_id)[0]

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        return self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))