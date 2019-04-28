from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import DataFile

@receiver(post_save, sender=DataFile)
def process_datafile(sender, instance, created, **kwargs):
    """Call an outside script whenever a DataFile is created to process the file."""
    if created:
        # this is where we want to call the ML sub-team's script
        pass

@receiver(pre_save, sender=DataFile)
def populate_datafile_hash(sender, instance, **kwargs):
    """
    Calculates the hash of the uploaded datafile before saving and populates the respective field in the model, if it hasn't already been populated by the Admin form or API.
    """
    if sender == DataFile and not instance.data_file_hash:
        print("got here")
        import hashlib
        sha256_hash = hashlib.sha256()
        # Read and update hash string value in blocks of 4K
        for chunk in instance.data_file.chunks():
            sha256_hash.update(chunk)
        instance.data_file_hash = sha256_hash.hexdigest()[:32]

@receiver(post_delete, sender=DataFile)
def delete_data_file_from_disk(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `DataFile` object is deleted.
    """
    import os
    if instance.processed_file:
        if os.path.isfile(instance.data_file.path):
            os.remove(instance.data_file.path)
    if instance.data_file:
        if os.path.isfile(instance.data_file.path):
            os.remove(instance.data_file.path)
