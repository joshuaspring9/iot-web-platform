from django.urls import path
from django.views.generic.base import TemplateView
from . import views


app_name = 'pages'
urlpatterns = [
    path('', views.index, name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
]
