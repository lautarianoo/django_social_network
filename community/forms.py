from django import forms
from .models import Group

class EditGroupForm(forms.ModelForm):

    privaty = forms.BooleanField(label='Закрытая', widget={'attrs': 'form-control'})
    status = forms.CharField(label='Статус', widget=forms.TextInput())
    description = forms.CharField(label='Описание', widget=forms.Textarea())
    website = forms.CharField(label='Сайт', widget=forms.URLInput())

    class Meta:
        model = Group
        fields = ('category', 'thematic', 'title', 'slug', )
