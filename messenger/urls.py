from django.urls import path
from .views import *

urlpatterns = [
    path('', AllMessages.as_view(), name='messages'),
    path('im', RoomView.as_view(), name='room_view'),
    path('seroo', SearchRoom.as_view(), name='searching-room'),
    path('dialog-add/<str:username>/', DialogAddView.as_view(), name='add-dialog'),
    path('create', ConferenceAddView.as_view(), name='conference-add'),
    path('add-member/<int:id>', AddConferenceMember.as_view(), name='conference-member-add'),
    path('conf-leave', LeaveConferenceView.as_view(), name='conference-leave')
]