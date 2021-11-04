from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .models import SocialUser
from .forms import EditProfileForm

class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})

class ProfileView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user == SocialUser.objects.get(username=kwargs.get('slug')):
            context['user'] = request.user
        else:
            context['user'] = ''
            context['user2'] =  SocialUser.objects.get(username=kwargs.get('slug'))
        return render(request, 'profiles/myprofile.html', context)

class EditProfile(View):

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
            return redirect('profile', username=user.username)
        return render(request, 'profiles/edit.html', {'form': form})

class FriendsView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/friends.html', {'users': request.user.friends.all()})

class FollowersView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'profiles/users.html', {'users': request.user.followers.all()})

class AcceptFriend(View):

    def get(self, request, *args, **kwargs):
        follower = SocialUser.objects.get(username=kwargs.get('username'))
        follower.friends.add(request.user)
        request.user.followers.remove(follower)
        request.user.friends.add(follower)
        return redirect('friends')

class SubscribeView(View):

    def get(self, request, *args, **kwargs):
        subscriber = SocialUser.objects.get(username=kwargs.get('username'))
        subscriber.followers.add(request.user)
        request.user.subscribers.add(subscriber)
        return redirect('profile', slug=kwargs.get('username'))

class DeleteFriend(View):

    def get(self, request, *args, **kwargs):
        friend = SocialUser.objects.get(username=kwargs.get('username'))
        friend.subscribers.add(request.user)
        request.user.friends.remove(friend)
        request.user.followers.add(friend)
        return redirect('profile', slug=kwargs.get('username'))
