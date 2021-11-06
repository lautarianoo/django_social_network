from django.shortcuts import redirect
from django.views.generic import View
from .models import InfoUser

class PermissionMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.is_authenticated:
            if not InfoUser.objects.filter(user=request.user):
                infouser = InfoUser.objects.create()
                request.user.infouser = infouser
                request.user.save()
        return super().dispatch(request, *args, **kwargs)
