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

class DataCapturingDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataCapturingDevice
        exclude = ('oauth_application',)

class DataFileSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    def validate(self, data):
        if 'data_file' in data and data['data_file']:
            import hashlib
            sha256_hash = hashlib.sha256()
            # Read and update hash string value in blocks of 4K
            for chunk in data['data_file'].chunks():
                sha256_hash.update(chunk)
            # stash the hash in the data so it can be inserted into the database
            data['data_file_hash'] = sha256_hash.hexdigest()[:32]
            # if the hash already exists, we have a duplicate file, so raise a form validation error
            if (self.instance is None or (self.instance is not None and data['data_file_hash'] != data.data_file_hash)) and DataFile.objects.filter(data_file_hash=data['data_file_hash']).exists():
                raise serializers.ValidationError({'data_file':"That file has already been uploaded."})
        return data

    class Meta:
        model = DataFile
        exclude = ('data_file_hash',)
