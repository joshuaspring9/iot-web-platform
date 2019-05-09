from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from django.core.files import File
from .models import DataFile

@receiver(post_save, sender=DataFile)
def process_datafile(sender, instance, created, **kwargs):
    """Call an outside script whenever a DataFile is created to process the file."""
    if created and not instance.processed:
        try:
            # this is where we want to call the ML sub-team's script
            import os
            import sys
            sys.path.insert(0, '../iot-intrusion-detection/Machine Learning Subteam')
            sys.path.insert(0, '../iot-intrusion-detection/Machine Learning Subteam/RandomForestRegressor')
            path, ext = os.path.splitext(instance.data_file.path)
            print(path +"ext: "+ ext)
            if ext == ".pcap":
                sys.path.insert(0, '../iot-intrusion-detection/Machine Learning Subteam/pcap_parser')
                import pcap_to_csv
                import csv_cutter
                print(instance.data_file.path)
                pcap_to_csv.parse_pcap(instance.data_file.path)
                csv_cutter.cut_csv(path + '.csv', path + '_out.csv', 0, 45)
                filename = os.path.splitext(os.path.basename(instance.data_file.name))[0]
                instance.data_file = File(file=open(path + '_out.csv'), name=filename + '_out.csv')
                if os.path.isfile(path + '_out.csv'):
                    os.remove(path + '_out.csv')
                instance.save()


            
            import RandomForestRegressor.trainPredictFormat
            trainer = RandomForestRegressor.trainPredictFormat.trainAndPredict()
            trainer.load_model_file('../iot-intrusion-detection/Machine Learning Subteam/RandomForestRegressor/iot_model.sav')
            predictions = trainer.make_prediction_on_file(instance.data_file.path, True)
            print(predictions)
            if predictions != []:
                instance.processed_file.save('results_datafile_id' + str(instance.id) +'.txt', ContentFile(str(predictions)))
                instance.processed = True
                instance.save()
        except:
            pass

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
        path, ext = os.path.splitext(instance.data_file.path)
        path = path[:path.index('_out')]

        if os.path.isfile(instance.data_file.path):
            os.remove(instance.data_file.path)
        if os.path.isfile(path + '.pcap'):
            os.remove(path + '.pcap')
        if os.path.isfile(path + '.csv'):
            os.remove(path + '.csv')
