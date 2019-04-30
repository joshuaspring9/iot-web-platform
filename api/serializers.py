from .models import DataFile, SmartHomeDevice, DataCapturingDevice
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
    id = serializers.ReadOnlyField()
    class Meta:
        model = SmartHomeDevice
        fields = '__all__'

class DataCapturingDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataCapturingDevice
        fields = ('id',)

class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = DataFile
        exclude = ('data_file_hash',)
