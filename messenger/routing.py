from django.urls import re_path

from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<room_slug>\w+)/$', ConferenceConsumer.as_asgi()),
]