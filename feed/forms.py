from django import forms
from .models import Feed, Comment

class AddFeedForm(forms.Form):

    content = forms.CharField(label='', required=False, widget=forms.TextInput())
    images = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'multiple': 'multiple'}))

    def clean(self):
        data = self.cleaned_data['content']
        if data:
            if len(data) >=7000:
                raise forms.ValidationError('Больше 7000 слов')
        return self.cleaned_data

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border'}),
            'text': forms.Textarea(attrs={'class': 'form-control border'})}
