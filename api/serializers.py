from .models import DataFile, SmartHomeDevice
from dashboard.models import CustomUser, UserProfile
from rest_framework import serializers

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile')

class SmartHomeDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SmartHomeDevice
        fields = '__all__'

class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    devices_captured = SmartHomeDeviceSerializer()
    class Meta:
        model = DataFile
        fields = '__all__'