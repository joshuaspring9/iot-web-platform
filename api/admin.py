from django.contrib import admin

# Register your models here.
from .models import DataFile, SmartHomeDevice

admin.site.register(DataFile)
admin.site.register(SmartHomeDevice)
