from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DataFile

@receiver(post_save, sender=DataFile)
def process_datafile(sender, instance, created, **kwargs):
    """Call an outside script whenever a DataFile is created to process the file."""
    if created:
        # this is where we want to call the ML sub-team's script
        pass
