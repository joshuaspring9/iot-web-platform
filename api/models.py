from django.db import models
from django.conf import settings

# Create your models here.
class DataFile(models.Model):

    data_file = models.FileField(upload_to=settings.MEDIA_ROOT+"data-files")
    processed = models.BooleanField()
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "File Name: " + self.data_file + " Start Time: " + self.start_time + " End Time: " + self.end_time