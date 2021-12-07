from django.shortcuts import render
from django.views import View
from .models import Group

class GroupsView(View):

    def get(self, request, *args, **kwargs):
        groups = Group.objects.filter(followers=request.user)
        return render(request, 'community/groups.html', {"groups": groups})

class SearchGroup(View):

    def get(self, request, *args, **kwargs):
        follow_group = Group.objects.filter(title__icontains=request.GET.get('tit'))
        groups = Group.objects.filter(title__icontains=request.GET.get('tit'))
        return render(request, 'community/search_groups.html', {'follow_group': follow_group, 'groups': groups})
