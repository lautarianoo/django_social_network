from django import forms

class EditProfileForm(forms.Form):

    status = forms.CharField(max_length=150, required=False)
    username = forms.CharField(max_length=40)
    first_name = forms.CharField(max_length=35)
    avatar = forms.ImageField(required=False)
    last_name = forms.CharField(max_length=40)
    phone = forms.CharField(max_length=25, required=False)
    birthday = forms.CharField(max_length=40, required=False)
    city = forms.CharField(max_length=40, required=False)
    work = forms.CharField(max_length=60, required=False)

