from django.shortcuts import render, redirect
from django.views import View
from .models import Group
from profiles.models import PhotosUser
from feed.forms import AddFeedForm
from feed.models import Feed
import random

class GroupsView(View):

    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(followers=request.user)
        return render(request, 'community/groups.html', {"groups": groups})

class SearchGroup(View):

    def get(self, request, *args, **kwargs):
        follow_group = Group.objects.filter(title__icontains=request.GET.get('tit'))
        groups = Group.objects.filter(title__icontains=request.GET.get('tit'))
        return render(request, 'community/search_groups.html', {'follow_group': follow_group, 'groups': groups})

class GroupView(View):

    def get(self, request, *args, **kwargs):
        form = AddFeedForm()
        group = Group.objects.get(slug=kwargs.get('slug'))
        feeds = Feed.objects.filter(group=group).order_by('-date_add')
        last_5_photo = PhotosUser.objects.filter(group=group).order_by('-pk')[:5]
        return render(request, 'community/group.html', {'group': group, 'last_5_photo': last_5_photo, 'form': form,
                                                        'feeds': feeds})

    def post(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs.get('slug'))
        form = AddFeedForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_feed = Feed.objects.create(content=data['content'])
            if request.FILES:
                for photo in request.FILES.getlist('images'):
                    new_photo = PhotosUser.objects.create(image=photo)
                    slug_photo = f"{group.slug}_{new_photo.id}%{random.randint(1, 10)}_{random.randint(1, 99999999)}"
                    new_photo.slug = slug_photo
                    new_photo.save()
                    new_feed.images.add(new_photo)
                    group.photos.add(new_photo)
            new_feed.save()
            group.feeds.add(new_feed)
            group.save()
            return redirect('group', slug=kwargs.get('slug'))

class FollowGroupView(View):

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs.get('slug'))
        group.followers.add(request.user)
        group.save()
        return redirect('group', slug=kwargs.get('slug'))

class UnfollowGroup(View):

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs.get('slug'))
        group.followers.remove(request.user)
        group.save()
        return redirect('group', slug=kwargs.get('slug'))

class ImageGroupView(View):

    def get(self, request, *args, **kwargs):
        photo = PhotosUser.objects.get(slug=request.GET.get('p'))
        group = Group.objects.get(slug=kwargs.get('slug'))
        return render(request, 'community/image.html', {'photo': photo, 'group': group})