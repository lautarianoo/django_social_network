from django.shortcuts import redirect
from django.views.generic import View
from .models import InfoUser, SubscribersUser, FollowersUser

class PermissionMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_authenticated:
            if not InfoUser.objects.filter(user=request.user):
                infouser = InfoUser.objects.create()
                request.user.infouser = infouser
                request.user.save()
            if not SubscribersUser.objects.filter(socialuser=request.user):
                subscribers = SubscribersUser.objects.create()
                request.user.subscribers = subscribers
                request.user.save()
            if not FollowersUser.objects.filter(socialuser=request.user):
                followers = FollowersUser.objects.create()
                request.user.followers= followers
                request.user.save()
        return super().dispatch(request, *args, **kwargs)
