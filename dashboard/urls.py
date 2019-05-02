from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .forms import CustomAuthForm

from . import views

app_name = 'dashboard'
urlpatterns = [
    path('accounts/profile/picture/', views.UpdateProfilePic.as_view(), name='profilepic'),
    path('dashboard/', views.dashboard_list, name='home'),
    path('dashboard/<int:data_file_id>/', views.dashboard, name="datafile_detail"),
    path('myaccount/', TemplateView.as_view(template_name='dashboard/account.html'), name='myaccount')
]
