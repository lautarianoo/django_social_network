from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from .models import Room, Message
from profiles.models import SocialUser

def get_second_member(room, user):
    second_member = [member for member in room.members.all() if member != user]
    return second_member[0]

class AllMessages(View):

    def get(self, request, *args, **kwargs):
        rooms_filter = Room.objects.filter(members=request.user)
        if 'act' in request.GET.keys() and request.GET.get('act') == 'noread':
            rooms_filter = [room for room in rooms_filter if room.noread_messages() != 0]
        return render(request, 'messenger/messages.html', {'rooms': rooms_filter})

class SearchRoom(View):

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.filter(title__icontains=request.GET.get('conf'))
        return render(request, 'messenger/messages.html', {'rooms': rooms})

class RoomView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        room = Room.objects.get(id=request.GET.get('sell'))
        if request.user not in room.members.all():
            return redirect('messages')
        context['messages'] = room.messages_room.order_by('date_add')
        context['room'] = room
        context['room_id'] = room.id
        context['username'] = request.user.username
        context['second_member_username'] = ''
        if not room.conference:
            second_member = [member for member in room.members.all() if member != request.user]
            context['second_member'] = second_member[0]
            context['second_member_username'] = second_member[0].username
        room.messages_room.filter(read=False).exclude(author=request.user).update(read=True)
        return render(request, 'messenger/room.html', context)

    def post(self, request, *args, **kwargs):
        pass

    def dispatch(self, request, *args, **kwargs):
        if not Room.objects.filter(slug=request.GET.get('sell'), members=request.user).exists() and not Room.objects.filter(id=request.GET.get('sell'), members=request.user).exists():
            return redirect('messages')
        return super().dispatch(request, *args, **kwargs)

class DialogAddView(View):

    def get(self, request, *args, **kwargs):
        second_member = SocialUser.objects.get(username=kwargs.get('username'))
        title = f"{request.user.full_name} {second_member.full_name}"
        if not Room.objects.filter(Q(first_user=request.user, second_user=second_member) | Q(first_user=second_member, second_user=request.user)).exists():
            room = Room.objects.create(title=title)
            room.members.add(request.user)
            room.members.add(second_member)
            room.first_user = request.user
            room.second_user = second_member
            room.save()
        else:
            room = Room.objects.filter(title__icontains=title).first()
        response = redirect('room_view')
        response['Location'] += '?sell=' + str(room.id)
        return response

class ConferenceAddView(View):

    def get(self, request, *args, **kwargs):
        friends = request.user.friends.all()
        return render(request, 'messenger/conference-create.html', {'friends': friends})

    def post(self, request, *args, **kwargs):
        if request.POST.get('title'):
             new_conference = Room.objects.create(title=request.POST.get('title'), conference=True)
        else:
             title = f"{SocialUser.objects.get(id=request.POST.getlist('friends')[0]).first_name}, {SocialUser.objects.get(id=request.POST.getlist('friends')[-1]).first_name}"
             new_conference = Room.objects.create(title=title, conference=True)
        new_conference.members.add(request.user)
        new_conference.admins.add(request.user)
        data = request.POST
        if data.getlist('friends') and len(data.getlist('friends')) > 1:
            for id_friend in data.getlist('friends'):
                friend = SocialUser.objects.get(id=id_friend)
                new_conference.members.add(friend)
        else:
            raise ValidationError('Выберите больше двух пользователей')
        if request.FILES.get('avatar'):
            new_conference.avatar = request.FILES.get('avatar')
        new_conference.save()
        response = redirect('room_view')
        response['Location'] += '?sell=' + str(new_conference.id)
        return response

class AddConferenceMember(View):

    def get(self, request, *args, **kwargs):
        conference = Room.objects.get(id=kwargs.get('id'))
        friends = request.user.friends.all()
        return render(request, 'messenger/conference-member-add.html', {'friends': friends, 'conference': conference})

    def post(self, request, *args, **kwargs):
        conference = Room.objects.get(id=kwargs.get('id'))
        data = request.POST
        if data.getlist('friends'):
            for id_friend in data.getlist('friends'):
                friend = SocialUser.objects.get(id=id_friend)
                if friend not in conference.members.all():
                    conference.members.add(friend)
            conference.save()
        response = redirect('room_view')
        response['Location'] += '?sell=' + str(conference.id)
        return response

class LeaveConferenceView(View):

    def get(self, request, *args, **kwargs):
        conference = Room.objects.get(id=request.GET.get('leave'))
        conference.members.remove(request.user)
        conference.save()
        return redirect('messages')