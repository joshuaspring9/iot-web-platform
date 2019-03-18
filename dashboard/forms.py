from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.widgets import PasswordInput, TextInput
from allauth.account.forms import LoginForm, SignupForm

from .models import CustomUser


class CustomUserCreationForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
   
    class Media:
        css = {
            'all': ('dashboard/login-form.css',),
        }

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomAuthForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = ''
        self.fields['password'].label = ''
    class Media:
        css = {
            'all': ('dashboard/login-form.css',),
        }
