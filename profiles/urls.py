from django.urls import path
from .views import *
from feed.views import AddFeedUser

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:slug>/', AddFeedUser.as_view(), name='add-feed'),
    path('profile/feed/delete_feed/<int:pk>/', DeleteFeedUser.as_view(), name='delete_feed'),
    path('edit/', EditProfile.as_view(), name='edit'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='subscribe'),
    path('add-friend/<str:username>/', AcceptFriend.as_view(), name='add-friend'),
    path('delete-friend/<str:username>/', DeleteFriend.as_view(), name='delete-friend'),
    path('unsubscribe/<str:username>/', Unsubscribe.as_view(), name='unsubscribe'),
    path('search/', MainSearchView.as_view(), name='search'),
    path('friends/search/', FriendSearchView.as_view(), name='search-friend')
]
