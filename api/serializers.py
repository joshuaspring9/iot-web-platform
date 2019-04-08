from .models import DataFile
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

class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataFile
        fields = '__all__'