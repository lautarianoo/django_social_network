from django.shortcuts import render, redirect
from django.views import View
from profiles.models import SocialUser
from feed.models import Feed
from feed.forms import CommentForm

class FeedView(View):

    def get(self, request, *args, **kwargs):
        feed = Feed.objects.get(id=request.GET.get('w'))
        form = CommentForm()
        request.session['feed_pk'] = feed.id
        return render(request, 'feed/feed.html', {'feed': feed, 'form': form})

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
        return redirect('profile', slug=request.user.username)

