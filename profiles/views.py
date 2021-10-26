from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View
from .models import SocialUser

class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})

class ProfileView(View):

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user == SocialUser.objects.get(username=kwargs.get('username')):
            context['user'] = request.user
        return render(request, 'profiles/myprofile.html', context)
