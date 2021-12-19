from django.urls import path
from .views import *

urlpatterns = [
    path('', AllMessages.as_view(), name='messages'),
]