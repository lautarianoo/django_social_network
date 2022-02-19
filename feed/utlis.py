from django.db.models import Q

from .models import Feed
from community.models import Group
from profiles.models import SocialUser

def filternews(user):
    no_sorted_news = []
    group_subscribe = Group.objects.filter(followers__in=[user]).distinct()
    for group in group_subscribe:
        for news in group.feeds.all():
            if news.user != user:
                no_sorted_news.append(news)
    friends_subscribe_user = SocialUser.objects.filter(Q(friends__in=[user]) | Q(subscribers__subscribers__in=[user])).distinct()
    for profile in friends_subscribe_user:
        for news in profile.feeds.all():
            if news.user != user:
                no_sorted_news.append(news)
    return no_sorted_news
