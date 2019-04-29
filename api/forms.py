from django import forms
from .models import DataFile

class DataFileForm(forms.ModelForm):

    class Meta:
        model = DataFile
        exclude = ('data_file_hash', )

    def clean(self):
        self.clean_data = super().clean()
        import hashlib
        sha256_hash = hashlib.sha256()
        # Read and update hash string value in blocks of 4K
        for chunk in self.cleaned_data['data_file'].chunks():
            sha256_hash.update(chunk)
        # stash the hash in the cleaned data so it can be inserted into the database
        self.cleaned_data['data_file_hash'] = sha256_hash.hexdigest()[:32]
        # if the hash already exists, we have a duplicate file, so raise a form validation error
        if (self.instance.pk == None or (self.instance.pk != None and self.cleaned_data['data_file_hash'] != self.instance.data_file_hash)) and DataFile.objects.filter(data_file_hash=self.cleaned_data['data_file_hash']).exists():
            raise forms.ValidationError({'data_file':"That file has already been uploaded."})
        return self.cleaned_data