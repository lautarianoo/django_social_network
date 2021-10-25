from django.urls import path
from .views import BaseView, ProfileView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile')
]
