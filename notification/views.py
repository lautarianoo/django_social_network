from django.http import JsonResponse
from django.shortcuts import render
from .models import Notification

def mark_notifications_as_read(request):
    Notification.objects.filter(reciever=request.user, type="comment").update(read=True)
    return JsonResponse({
        'status': True,
        'message': "Marked all notifications as read"
    })
