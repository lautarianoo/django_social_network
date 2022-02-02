from django.urls import path
from .views import *

urlpatterns = [
    path('', FeedView.as_view(), name='feed'),
    path('add-comment/<int:pk>/', AddComment.as_view(), name='add-comment'),
    path('repost-feed-page/<int:id>', RepostOnPageView.as_view(), 'repost-feed-page')
]
