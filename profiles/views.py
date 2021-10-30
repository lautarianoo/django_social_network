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
        if request.user == SocialUser.objects.get(username=kwargs.get('username')):
            context['user'] = request.user
        return render(request, 'profiles/myprofile.html', context)

class EditProfile(View):

    def get(self, request, *args, **kwargs):
        form = EditProfileForm(initial={'username': request.user.username, 'first_name': request.user.first_name,
                                        'avatar': request.user.avatar, 'last_name': request.user.last_name, 'phone': request.user.phone,
                                        'birthday': request.user.infouser.birthday, 'city': request.user.infouser.city, 'status': request.user.infouser, 'work': request.user.infouser.city})
        return render(request, 'profiles/edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data

            user = request.user
            user.username = data['username']
            user.first_name = data['first_name']
            user.avatar = data['avatar']
            user.last_name = data['last_name']
            user.phone = data['phone']
            user.infouser.birthday = data['birthday']
            user.infouser.city = data['city']
            user.infouser.status = data['status']
            user.infouser.work = data['work']
            user.save()
            return redirect('profile', username=user.username)
        return render(request, 'profiles/edit.html', {'form': form})
