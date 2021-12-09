from django.urls import path
from .views import *

urlpatterns = [
    path('', GroupsView.as_view(), name='groups'),
    path('search', SearchGroup.as_view(), name='search-groups'),
    path('<str:slug>/', GroupView.as_view(), name='group'),
    path('follow/<str:slug>/', FollowGroupView.as_view(), name='follow-group'),
    path('unfollow/<str:slug>/', UnfollowGroup.as_view(), name='unfollow-group'),
    path('<str:slug>/im', ImageGroupView.as_view(), name='image-group')
]
