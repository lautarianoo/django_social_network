import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from profiles.models import SocialUser
from feed.models import Feed
from feed.forms import CommentForm
from community.models import Group
from notification.models import Notification
from notification.serializers import NotificationSerializer
from .utlis import filternews

class FeedView(View):

    def get(self, request, *args, **kwargs):
        feed = Feed.objects.get(id=request.GET.get('w'))
        group = Group.objects.filter(feeds=feed).first()
        user = SocialUser.objects.filter(feeds=feed).first()
        form = CommentForm()
        request.session['feed_pk'] = feed.id
        return render(request, 'feed/feed.html', {'feed': feed, 'form': form, 'group': group, 'user': user})

class AddComment(View):

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            if request.POST.get('parent', None):
                new_comment.parents.add(request.POST.get('parent'))
            new_comment.save()
            feed = Feed.objects.get(id=kwargs.get('pk'))
            feed.comments.add(new_comment)
            feed_author = SocialUser.objects.get(feeds=feed)
            if feed_author != request.user:
                notification = Notification.objects.create(type="comment", reciever=feed_author, author=request.user,
                                                           verb="написал(а) комментарий к вашей записи")
                channel_layer = get_channel_layer()
                channel = f"new_comment_notification_{feed_author.username}"
                async_to_sync(channel_layer.group_send)(
                    channel, {
                        "type": "notify",
                        "command": "new_comment_notification",
                        "notification": json.dumps(NotificationSerializer(notification).data)
                    }
                )
        return redirect('profile', slug=request.user.username)

class RepostOnPageView(View):

    def get(self, request, *args, **kwargs):
        reposted_feed = Feed.objects.get(id=kwargs.get('id'))
        new_feed = Feed.objects.create(reposted_feed=reposted_feed, reposted=True)
        new_feed.save()
        request.user.feeds.add(new_feed)
        return redirect('profile', slug=request.user.username)

class NewsLentaView(View):

    def get(self, request, *args, **kwargs):
        news_user = filternews(request.user)
        print(news_user[0].user.username)
        return render(request, 'feed/news.html', {'news': news_user})