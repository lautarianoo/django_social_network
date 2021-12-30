from django.urls import path
from .views import *

urlpatterns = [
    path('', AllMessages.as_view(), name='messages'),
    path('im', RoomView.as_view(), name='room_view'),
    path('seroo', SearchRoom.as_view(), name='searching-room')
]