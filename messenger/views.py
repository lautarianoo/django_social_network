from django.shortcuts import render
from django.views import View
from .models import Room, Message

class AllMessages(View):

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.filter(members=request.user)
        return render(request, 'messenger/messages.html', {'rooms': rooms})