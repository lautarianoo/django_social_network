import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from feed.models import Feed
from messenger.models import Room
from notification.serializers import NotificationSerializer
from .models import SocialUser, InfoUser, SubscribersUser, FollowersUser
from .forms import EditProfileForm, LoginForm, RegisterForm
from .mixins import PermissionMixin
from community.models import Group
from feed.forms import AddFeedForm
from .models import PhotosUser
import random
from notification.models import Notification
#class BaseView(View):
#
#    def get(self, request, *args, **kwargs):
#        return render(request, 'base.html', {})#all'})

class MainSearchView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['get_name'] = request.GET.get('q')
        users = SocialUser.objects.filter(full_name__icontains=request.GET.get('q'))
        community = Group.objects.filter(title__icontains=request.GET.get('q'))
        first_5_users = [users[user] for user in range(len(users)) if user <= 5]
        context['first_5_users'] = first_5_users
        first_5_group = [community[group] for group in range(len(community)) if group <= 5]
        context['first_5_group'] = first_5_group
        context['users'] = ''
        context['communities'] = ''
        if 'section' in request.GET.keys() and request.GET.get('section') == 'all':
            context['get_all'] = '1'
        elif 'section' in request.GET.keys() and request.GET.get('section') == 'people':
            context['users'] = users
        elif 'section' in request.GET.keys() and request.GET.get('section') == 'community':
            context['communities'] = community
        else:
            context['get_all2'] = '1'
        return render(request, 'searching.html', context)

class FriendSearchView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        friends = SocialUser.objects.filter(full_name__icontains=request.GET.get('q'), friends=request.user)
        users = SocialUser.objects.filter(full_name__icontains=request.GET.get('q'))
        context['friends'] = friends
        context['users'] = users
        return render(request, 'profiles/search-friend.html', context)

class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', slug=request.user.username)
        form = LoginForm()
        return render(request, 'profiles/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('profile', slug=user.username)
        return render(request, 'profiles/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

class RegisterView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', slug=request.user.username)
        form = RegisterForm()
        return render(request, 'profiles/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            infouser = InfoUser.objects.create()
            infouser.city = ''
            infouser.status = ''
            infouser.birthday = ''
            infouser.work = ''
            new_user.infouser = infouser
            subscribers = SubscribersUser.objects.create()
            followers = FollowersUser.objects.create()
            new_user.subscribers = subscribers
            new_user.followers = followers
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            return HttpResponseRedirect(reverse('login'))
        return render(request, 'profiles/register.html', {'form': form})


class ProfileView(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        form = AddFeedForm()
        context['form'] = form
        if request.user == SocialUser.objects.get(username=kwargs.get('slug')):
            context['user'] = request.user
            context['feedss'] = Feed.objects.filter(user=request.user).order_by('-date_add')
            last_5_photo = PhotosUser.objects.filter(user=request.user).order_by('-pk')[:5]
            context['last_6_friends'] = SocialUser.objects.filter(friends=request.user).order_by('-pk')[:6]
            context['last_5_groups'] = Group.objects.filter(followers=request.user)
            context['last_5_photo'] =last_5_photo
        else:
            context['user'] = ''
            user2 = SocialUser.objects.get(username=kwargs.get('slug'))
            context['user2'] =  user2
            context['general_friends'] = []
            for friend in user2.friends.all():
                if friend in request.user.friends.all():
                    context['general_friends'].append(friend)
            context['len_general_friends'] = len(context['general_friends'])
            context['last_6_friends'] = SocialUser.objects.filter(friends=user2).order_by('-pk')[:6]
            context['last_5_groups'] = Group.objects.filter(followers=user2)
            context['feedss'] = Feed.objects.filter(user=user2).order_by('-date_add')
            last_5_photo = PhotosUser.objects.filter(user=user2).order_by('-pk')[:5]
            context['last_5_photo'] = last_5_photo
        return render(request, 'profiles/myprofile.html', context)

    def post(self, request, *args, **kwargs):
        form = AddFeedForm(request.POST or None, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_feed = Feed.objects.create(content=data['content'])
            if request.FILES:
                for photo in request.FILES.getlist('images'):
                    new_photo = PhotosUser.objects.create(image=photo)
                    slug_photo = f"{request.user.username}_{new_photo.id}%{random.randint(1, 10)}_{random.randint(1, 99999999)}"
                    new_photo.slug = slug_photo
                    new_photo.save()
                    request.user.photos.add(new_photo)
                    new_feed.images.add(new_photo)
            new_feed.save()
            request.user.feeds.add(new_feed)
            request.user.save()
            return redirect('profile', slug=request.user.username)

class DeleteFeedUser(View):

    def get(self, request, *args, **kwargs):
        feed = Feed.objects.get(id=kwargs.get('pk'))
        request.user.feeds.remove(feed)
        feed.delete()
        return redirect('profile', slug=request.user.username)

class EditProfile(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        form = EditProfileForm(initial={'username': request.user.username, 'first_name': request.user.first_name,
                                        'avatar': request.user.avatar, 'last_name': request.user.last_name, 'phone': request.user.phone,
                                        'birthday': request.user.infouser.birthday, 'city': request.user.infouser.city, 'status': request.user.infouser.status, 'work': request.user.infouser.city})
        return render(request, 'profiles/edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data
            user = request.user
            user.username = data['username']
            user.first_name = data['first_name']
            if data['avatar']:
                user.avatar = data['avatar']
            else:
                user.avatar = request.user.avatar
            user.last_name = data['last_name']
            user.phone = data['phone']
            user.infouser.birthday = data['birthday']
            user.infouser.city = data['city']
            user.infouser.status = data['status']
            user.infouser.work = data['work']
            user.infouser.save()
            user.save()
            return redirect('profile', slug=user.username)
        return render(request, 'profiles/edit.html', {'form': form})

class FriendsView(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        context = {}
        context['users'] = request.user.friends.all()
        if 'act' in request.GET.keys():
            possible_friends = set()
            for friend in request.user.friends.all():
                for genfriend in friend.friends.all():
                    if genfriend not in request.user.friends.all() and genfriend != request.user:
                        possible_friends.add(genfriend)
            context['possible_friends'] = possible_friends
            print(context['possible_friends'])
        else:
            context['possible_friends'] = ''
        return render(request, 'profiles/friends.html', context)

class FollowersView(PermissionMixin, View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/users.html', {'users': request.user.followers.followers.all()})

class SubscribersView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/subscribers.html', {"users": request.user.subscribers.subscribers.all()})

class SubscribeView(View):

    def get(self, request, *args, **kwargs):
        subscriber = SocialUser.objects.get(username=kwargs.get('username'))
        subscriber.followers.followers.add(request.user)
        request.user.subscribers.subscribers.add(subscriber)
        notification = Notification.objects.create(type="friend", reciever=subscriber, author=request.user,
                                                   verb=f"{request.user.first_name} {request.user.last_name} отправил заявку в друзья")
        channel_layer = get_channel_layer()
        channel = f"notifications_{subscriber.username}"
        async_to_sync(channel_layer.group_send)(
            channel, {
                'type': 'notify',
                'command': 'new_notification',
                'notification': json.dumps(NotificationSerializer(notification).data)
            }
        )
        data = {
            'status': True,
            'message': 'Request sent',
        }
        return JsonResponse(data)

class AcceptFriend(View):

    def get(self, request, *args, **kwargs):
        follower = SocialUser.objects.get(username=kwargs.get('username'))
        request.user.followers.followers.remove(follower)
        follower.subscribers.subscribers.remove(request.user)
        request.user.friends.add(follower)
        follower.friends.add(request.user)
        title = f"{request.user.id} {follower.id}"
        if not Room.objects.filter(Q(first_user=request.user, second_user=follower) | Q(first_user=follower, second_user=request.user)).exists():
            room = Room.objects.create(title=title)
            room.members.add(request.user)
            room.members.add(follower)
            room.first_user = request.user
            room.second_user = follower
            room.save()

        Notification.objects.filter(reciever=request.user, author=follower).delete()
        data = {
            'status': True,
            'message': 'You accepted friend request'
        }
        return JsonResponse(data)

class DeleteFriend(View):

    def get(self, request, *args, **kwargs):
        friend = SocialUser.objects.get(username=kwargs.get('username'))
        friend.friends.remove(request.user)
        request.user.friends.remove(friend)
        friend.subscribers.subscribers.add(request.user)
        request.user.followers.followers.add(friend)
        return redirect('profile', slug=kwargs.get('username'))

class Unsubscribe(View):

    def get(self, request, *args, **kwargs):
        subscriber = SocialUser.objects.get(username=kwargs.get('username'))
        subscriber.followers.followers.remove(request.user)
        request.user.subscribers.subscribers.remove(subscriber)
        return redirect('profile', slug=kwargs.get('username'))

class ImageView(View):

    def get(self, request, *args, **kwargs):
        image = PhotosUser.objects.get(slug=request.GET.get('p'))
        user = SocialUser.objects.get(username=kwargs.get('slug'))
        return render(request, 'profiles/image.html', {'image': image, 'user': user})

