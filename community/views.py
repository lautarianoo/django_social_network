from django.shortcuts import render, redirect
from django.views import View
from .models import Group, InfoGroup
from profiles.models import PhotosUser
from feed.forms import AddFeedForm
from feed.models import Feed
import random
from .forms import EditGroupForm

class GroupsView(View):

    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(followers=request.user)
        return render(request, 'community/groups.html', {"groups": groups})

class SearchGroup(View):

    def get(self, request, *args, **kwargs):
        follow_group = Group.objects.filter(title__icontains=request.GET.get('tit'), followers=request.user)
        groups = Group.objects.filter(title__icontains=request.GET.get('tit'))
        return render(request, 'community/search_groups.html', {'follow_group': follow_group, 'groups': groups})

class EditGroupView(View):

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs.get('slug'))
        form = EditGroupForm(initial={'status': group.infogroup.status, 'privaty': group.infogroup.privaty, 'description': group.infogroup.description,
                                      'website': group.infogroup.website, 'category': group.category, 'thematic': group.thematic, 'title': group.title, 'avatar': group.avatar,
                                      'slug': group.slug})
        return render(request, 'community/edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditGroupForm(request.POST, request.FILES or None)
        if form.is_valid():
            data = form.cleaned_data
            group = Group.objects.get(slug=kwargs.get('slug'))
            group.infogroup.privaty = data['privaty']
            group.infogroup.description = data['description']
            group.infogroup.status = data['status']
            group.infogroup.website = data['website']
            group.infogroup.save()
            group.category = data['category']
            group.thematic = data['thematic']
            group.title = data['title']
            if data['avatar']:
                group.avatar = data['avatar']
            group.slug = data['slug']
            group.save()
            return redirect('group', slug=kwargs.get('slug'))
        return render(request, 'community/edit.html', {'form': form})

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

class DeleteFeedGroup(View):

    def get(self, request, *args, **kwargs):
        feed = Feed.objects.get(id=kwargs.get('pk'))
        group = Group.objects.get(feeds=feed)
        group.feeds.remove(feed)
        feed.delete()
        return redirect('group', slug=group.slug)

class FollowGroupView(View):

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs.get('slug'))
        if group.infogroup.privaty:
            group.applications.add(request.user)
        else:
            group.followers.add(request.user)
        group.save()
        return redirect('group', slug=kwargs.get('slug'))

class UnfollowGroup(View):

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs.get('slug'))
        if group.infogroup.privaty and request.user not in group.followers.all():
            group.applications.remove(request.user)
        else:
            group.followers.remove(request.user)
        group.save()
        return redirect('group', slug=kwargs.get('slug'))

class ImageGroupView(View):

    def get(self, request, *args, **kwargs):
        photo = PhotosUser.objects.get(slug=request.GET.get('p'))
        group = Group.objects.get(slug=kwargs.get('slug'))
        return render(request, 'community/image.html', {'photo': photo, 'group': group})