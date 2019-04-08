from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class DataFile(models.Model):

    # Note that while only PCAP extensions, are allowed, ANY file can be renamed to .pcap and be accepted.
    # TODO: implement stricter file validation
    data_file = models.FileField(upload_to='media/data-files', validators=[FileExtensionValidator(allowed_extensions=['pcap'])])
    processed = models.BooleanField()
    processed_file = models.FileField(upload_to='media/data-files')
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "File Name: " + self.data_file + " Start Time: " + self.start_time + " End Time: " + self.end_time
