from django.shortcuts import render, redirect
from django.views import View
from .models import Group
from profiles.models import PhotosUser

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
        group = Group.objects.get(slug=kwargs.get('slug'))
        last_5_photo = PhotosUser.objects.filter(group=group).order_by('-pk')[:5]
        return render(request, 'community/group.html', {'group': group, 'last_5_photo': last_5_photo})

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