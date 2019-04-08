from django.shortcuts import render
from dashboard.models import CustomUser, UserProfile
from .models import DataFile
from rest_framework import viewsets
from .serializers import UserSerializer, UserProfileSerializer, DataFileSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class DataFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data files to be viewed or edited.
    """
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
