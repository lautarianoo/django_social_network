from django.urls import path
from .views import *

urlpatterns = [
    path('mark_like_comment_notifications_as_read', mark_like_comment_notifications_as_read, name='mark_like_comment_notifications_as_read')
]