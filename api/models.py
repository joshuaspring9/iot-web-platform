from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class SmartHomeDevice(models.Model):
    '''
    Class to represent a smart home device.  Used with data files to represent the devices captured.
    '''

    name = models.CharField(max_length=75)
    image = models.ImageField(blank=True, null=True, upload_to="device-pictures")
    description = models.CharField(max_length=256, blank=True, null=True)

    def has_device_image(self):
        return self.image != ""

    def __str__(self):
        return self.name


class DataFile(models.Model):
    '''
    Class to represent a network data capture file
    '''
    # Note that while only PCAP extensions, are allowed, ANY file can be renamed to .pcap and be accepted.
    # TODO: implement stricter file validation
    data_file = models.FileField(upload_to='data-files', validators=[FileExtensionValidator(allowed_extensions=['pcap'])])
    data_file_hash = models.CharField(max_length=35, unique=True)
    devices_captured = models.ManyToManyField(SmartHomeDevice)
    processed = models.BooleanField()
    processed_file = models.FileField(upload_to='data-files-processed', null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def is_processed(self):
        return self.processed

    def __str__(self):
        return str(self.data_file)
