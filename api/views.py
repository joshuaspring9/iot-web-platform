from django.shortcuts import render
from dashboard.models import CustomUser, UserProfile
from rest_framework import viewsets
from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope
from .models import DataFile, SmartHomeDevice, DataCapturingDevice
from .serializers import UserSerializer, UserProfileSerializer, DataFileSerializer, SmartHomeDeviceSerializer, DataCapturingDeviceSerializer
from .permissions import IsAdminOrHasModelPermissionsOrTokenHasScope, IsAdminOrHasModelPermissionsOrTokenHasRWScope
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasRWScope]
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class SmartHomeDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows smart home devices to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasRWScope|TokenHasScope]
    required_scopes =  ['devices']
    queryset = SmartHomeDevice.objects.all()
    serializer_class = SmartHomeDeviceSerializer

class DataCapturingDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data capturing devices to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasRWScope|TokenHasScope]
    required_scopes = ['devices']
    queryset = DataCapturingDevice.objects.all()
    serializer_class = DataCapturingDeviceSerializer

class DataFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data files to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasScope]
    required_scopes = ['datafiles']
    
    def get_queryset(self):
        queryset = DataFile.objects.all()
        # if the token used represents a device, only show data files uploaded by that device
        if hasattr(self.request, 'auth') and hasattr(self.request.auth, "application") and hasattr(self.request.auth.application, "datacapturingdevice") and hasattr(self.request.auth.application, "authorization_grant_type") and self.request.auth.application.authorization_grant_type == "client-credentials":
            queryset = queryset.filter(data_capturing_device=self.request.auth.application.datacapturingdevice)
        return queryset

    serializer_class = DataFileSerializer       
