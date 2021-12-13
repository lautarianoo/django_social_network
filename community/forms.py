from django import forms
from .models import Group

class EditGroupForm(forms.ModelForm):

    privaty = forms.BooleanField(label='Закрытая')
    status = forms.CharField(label='Статус', widget=forms.TextInput())
    description = forms.CharField(label='Описание', widget=forms.Textarea())
    website = forms.CharField(label='Сайт', widget=forms.URLInput())
    avatar = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = Group
        fields = ('category', 'thematic', 'title', 'slug', )

    def __init__(self, *args, **kwargs):
        super(EditGroupForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False