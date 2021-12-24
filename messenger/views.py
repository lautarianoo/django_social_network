from django.shortcuts import render, redirect
from django.views import View
from .models import Room, Message
from profiles.models import SocialUser

class AllMessages(View):

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.filter(members=request.user)
        return render(request, 'messenger/messages.html', {'rooms': rooms})

class RoomView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        if  Room.objects.filter(slug=request.GET.get('sell')).exists():
            room = Room.objects.get(slug=request.GET.get('sell'))
            context['room'] = room
        else:
            room = Room.objects.get(id=request.GET.get('sell'))
            context['room'] = room
            context['room_id'] = room.id
            second_member = [member for member in room.members.all() if member != request.user]
            context['second_member'] = second_member[0]
        room.messages_room.filter(read=False).exclude(author=request.user).update(read=True)
        return render(request, 'messenger/room.html', context)

    def post(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        if not Room.objects.filter(slug=request.GET.get('sell'), members=request.user).exists() and not Room.objects.filter(id=request.GET.get('sell'), members=request.user).exists():
            return redirect('messages')
        return super().dispatch(request, *args, **kwargs)

