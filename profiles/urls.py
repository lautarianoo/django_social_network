from django.urls import path
from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('edit/', EditProfile.as_view(), name='edit'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('add-friend/<str:username>/', AcceptFriend.as_view(), name='add-friend'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='subscribe'),
    path('delete-friend/<str:username>/', DeleteFriend.as_view(), name='delete-friend')
]
