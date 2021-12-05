from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('profile/feed/delete_feed/<int:pk>/', DeleteFeedUser.as_view(), name='delete_feed'),
    path('edit/', EditProfile.as_view(), name='edit'),
    path('friends', FriendsView.as_view(), name='friends'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='subscribe'),
    path('add-friend/<str:username>/', AcceptFriend.as_view(), name='add-friend'),
    path('delete-friend/<str:username>/', DeleteFriend.as_view(), name='delete-friend'),
    path('unsubscribe/<str:username>/', Unsubscribe.as_view(), name='unsubscribe'),
    path('search', MainSearchView.as_view(), name='search'),
    path('friends/search/', FriendSearchView.as_view(), name='search-friend'),
    path('profile/<str:slug>', ImageView.as_view(), name='image'),
]

#x, y = int(input()), int(input())
#sign = input()
#if sign in '+-*/':
#    if sign == '+':
#        print(x+y)
#    if sign == '-':
#        print(x-y)
#    if sign == '*':
#        print(x*y)
#    if sign == '/' and y!=0:
#        print(x/y)
#    else:
#        print('На ноль делить нельзя')
#else:
#    print('Неверная операция')
