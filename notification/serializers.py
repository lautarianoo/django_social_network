from rest_framework import serializers
from profiles.serializers import UserSerializer
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = "__all__"