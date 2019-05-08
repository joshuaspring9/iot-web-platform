from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from .models import DataFile

@receiver(post_save, sender=DataFile)
def process_datafile(sender, instance, created, **kwargs):
    """Call an outside script whenever a DataFile is created to process the file."""
    if created and not instance.processed:
        # this is where we want to call the ML sub-team's script
        import sys
        sys.path.insert(0, '../iot-intrusion-detection/Machine Learning Subteam')
        sys.path.insert(0, '../iot-intrusion-detection/Machine Learning Subteam/RandomForestRegressor')
        import RandomForestRegressor.trainPredictFormat
        trainer = RandomForestRegressor.trainPredictFormat.trainAndPredict()
        trainer.load_model_file('../iot-intrusion-detection/Machine Learning Subteam/RandomForestRegressor/iot_model.sav')
        predictions = trainer.make_prediction_on_file(instance.data_file.path, True)
        instance.processed_file.save('results_datafile_id' + str(instance.id) +'.txt', ContentFile(str(predictions)))
        instance.processed = True
        instance.save()

@receiver(pre_save, sender=DataFile)
def populate_datafile_hash(sender, instance, **kwargs):
    """
    Calculates the hash of the uploaded datafile before saving and populates the respective field in the model, if it hasn't already been populated by the Admin form or API.
    """
    if sender == DataFile and not instance.data_file_hash and instance.data_file:
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
