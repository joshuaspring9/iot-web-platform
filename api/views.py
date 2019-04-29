from django.shortcuts import render
from dashboard.models import CustomUser, UserProfile
from .models import DataFile, SmartHomeDevice
from rest_framework import viewsets
from .serializers import UserSerializer, UserProfileSerializer, DataFileSerializer, SmartHomeDeviceSerializer
from .permissions import IsAdminOrHasModelPermissionsOrTokenHasScope
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasScope]
    queryset = CustomUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class SmartHomeDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows smart home devices to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasScope]
    queryset = SmartHomeDevice.objects.all()
    serializer_class = SmartHomeDeviceSerializer

class DataFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows data files to be viewed or edited.
    """
    permission_classes = [IsAdminOrHasModelPermissionsOrTokenHasScope]

    def get_queryset(self):
        queryset = DataFile.objects.all()
        # if the token used represents a device, only show data files uploaded by that device
        if hasattr(self.request, 'auth') and hasattr(self.request.auth, "application") and hasattr(self.request.auth.application, "datacapturingdevice") and hasattr(self.request.auth.application, "authorization_grant_type") and self.request.auth.application.authorization_grant_type == "client-credentials":
            queryset = queryset.filter(data_capturing_device=self.request.auth.application.datacapturingdevice)
        return queryset

    serializer_class = DataFileSerializer        
