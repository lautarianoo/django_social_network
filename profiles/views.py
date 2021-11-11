from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import SocialUser, InfoUser, SubscribersUser, FollowersUser
from .forms import EditProfileForm, LoginForm, RegisterForm
from .mixins import PermissionMixin

#class BaseView(View):
#
#    def get(self, request, *args, **kwargs):
#        return render(request, 'base.html', {})

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
        if request.user == SocialUser.objects.get(username=kwargs.get('slug')):
            context['user'] = request.user
        else:
            context['user'] = ''
            context['user2'] =  SocialUser.objects.get(username=kwargs.get('slug'))
        return render(request, 'profiles/myprofile.html', context)

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
        return render(request, 'profiles/friends.html', {'users': request.user.friends.all()})

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
        return redirect('profile', slug=kwargs.get('username'))

class AcceptFriend(View):

    def get(self, request, *args, **kwargs):
        follower = SocialUser.objects.get(username=kwargs.get('username'))
        request.user.followers.followers.remove(follower)
        follower.subscribers.subscribers.remove(request.user)
        request.user.friends.add(follower)
        follower.friends.add(request.user)
        return redirect('profile', slug=kwargs.get('username'))

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



