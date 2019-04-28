from django.contrib import admin

# Register your models here.
from .models import DataFile, SmartHomeDevice

class DataFileAdmin(admin.ModelAdmin):
    exclude = ('data_file_hash',)

admin.site.register(DataFile, DataFileAdmin)
admin.site.register(SmartHomeDevice)
