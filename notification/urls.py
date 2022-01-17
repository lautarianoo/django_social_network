from django.urls import path
from .views import *

urlpatterns = [
    path('mark_notifications_as_read', mark_notifications_as_read, name='mark_notifications_as_read')
]