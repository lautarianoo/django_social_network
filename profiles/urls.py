from django.urls import path
from .views import *

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('edit/', EditProfile.as_view(), name='edit'),
    path('friends/', FriendsView.as_view(), name='friends'),
    path('followers/', FollowersView.as_view(), name='followers'),
    path('subscribers/', SubscribersView.as_view(), name='subscribers'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='subscribe'),
    path('add-friend/<str:username>/', AcceptFriend.as_view(), name='add-friend'),
    path('delete-friend/<str:username>/', DeleteFriend.as_view(), name='delete-friend'),
    path('unsubscribe/<str:username>/', Unsubscribe.as_view(), name='unsubscribe'),
]
