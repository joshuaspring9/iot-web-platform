from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .forms import CustomAuthForm

from . import views

app_name='dashboard'
urlpatterns = [
    path('', TemplateView.as_view(template_name='dashboard/home.html'), name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html', authentication_form=CustomAuthForm), name='login'),
]
