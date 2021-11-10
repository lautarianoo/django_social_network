from django import forms
from .models import SocialUser

class LoginForm(forms.Form):

    email = forms.CharField(label='Почта', widget=forms.EmailInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        if not SocialUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Такого пользователя не существует')
        user = SocialUser.objects.filter(email=email).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput())

    class Meta:
        model = SocialUser
        fields = ('username', 'email', 'phone', 'first_name', 'last_name')

    def clean_password2(self):
        data = self.cleaned_data
        if data['password1'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

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

