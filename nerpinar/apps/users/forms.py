from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class LoginForm(forms.Form): # для входа
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class RegisterForm(UserCreationForm): # для регистрации нового пользователя
    email = forms.EmailField(required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

