from django.urls import path
from .views import *

urlpatterns = [
    path('', GroupsView.as_view(), name='groups'),
    path('search', SearchGroup.as_view(), name='search-groups')
]
