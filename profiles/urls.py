from django.urls import path
from .views import BaseView, ProfileView, EditProfile

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('profile/<str:slug>/', ProfileView.as_view(), name='profile'),
    path('edit/', EditProfile.as_view(), name='edit'),
]
