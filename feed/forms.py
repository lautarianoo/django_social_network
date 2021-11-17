from django import forms
from .models import Feed

class AddFeedForm(forms.ModelForm):

    class Meta:
        model = Feed
        fields = ('content', )
