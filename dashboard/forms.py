from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.widgets import PasswordInput, TextInput
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label='', max_length=254, widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=PasswordInput(attrs={'placeholder': _("Password")}))
    class Media:
        css = {
            'all': ('dashboard/login-form.css',),
        }
