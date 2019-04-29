from django.contrib import admin
from .forms import DataFileForm

# Register your models here.
from .models import DataFile, SmartHomeDevice, DataCapturingDevice

class DataFileAdmin(admin.ModelAdmin):
    form = DataFileForm
    # override the save method to include the data_file_hash
    def save_model(self, request, obj, form, change):
        if 'data_file_hash' in form.cleaned_data:
            obj.data_file_hash = form.cleaned_data['data_file_hash']
        obj.save()

admin.site.register(DataFile, DataFileAdmin)
admin.site.register(SmartHomeDevice)
admin.site.register(DataCapturingDevice)
