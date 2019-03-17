from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext, ugettext_lazy as _
from django.forms.widgets import PasswordInput, TextInput
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username'
        })
        self.fields['username'].label = ''
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password'
        })
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Password Confirmation'
        })
        self.fields['password2'].label = ''
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email'
        })
        self.fields['email'].label = ''

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', )
    
    class Media:
        css = {
            'all': ('dashboard/login-form.css',),
        }

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
