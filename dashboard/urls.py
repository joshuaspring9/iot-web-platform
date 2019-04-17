from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('accounts/profile/picture/', views.UpdateProfilePic.as_view(), name='profilepic'),
    path('dashboard/', views.DashboardView.as_view(), name='home')
]
