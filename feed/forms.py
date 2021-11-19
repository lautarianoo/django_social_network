from django import forms
from .models import Feed
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AddFeedForm(forms.Form):

    content = forms.CharField(label='', required=True, widget=forms.TextInput())

    def clean(self):
        data = self.cleaned_data['content']
        if data:
            if len(data) >=7000:
                raise forms.ValidationError('Больше 7000 слов')
        return self.cleaned_data
