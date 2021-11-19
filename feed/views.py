from django.shortcuts import render, redirect
from django.views import View
from .forms import AddFeedForm
from profiles.models import SocialUser

class AddFeedUser(View):

    def get(self, request, *args, **kwargs):
        form = AddFeedForm()
        return render(request, 'profiles/myprofile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddFeedForm(request.POST or None)
        if form.is_valid():
            new_feed = form.save(commit=False)
            new_feed.save()
            request.user.feeds.add(new_feed)
            request.user.save()
            return redirect('profile', slug=request.user.username)
