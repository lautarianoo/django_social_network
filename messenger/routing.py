from django.urls import re_path

from .consumers import *

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'^ws/conference/(?P<room_slug>[^/]+)/$', ConferenceConsumer.as_asgi()),
]