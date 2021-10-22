from django.shortcuts import render
from django.views import View

class BaseView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})
