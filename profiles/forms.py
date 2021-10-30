from django import forms

class EditProfileForm(forms.Form):

    status = forms.CharField(max_length=150)
    username = forms.CharField(max_length=40)
    first_name = forms.CharField(max_length=35)
    avatar = forms.ImageField()
    last_name = forms.CharField(max_length=40)
    phone = forms.CharField(max_length=25)
    birthday = forms.CharField(max_length=40)
    city = forms.CharField(max_length=40)
    work = forms.CharField(max_length=60)
