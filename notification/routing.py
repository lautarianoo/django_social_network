from django.urls import re_path

from .consumers import *

websocket_urlpatterns = [
    re_path(r'^ws/like_photo_notification/$', NotificationConsumer.as_asgi()),
]