from django.db import models
from django.urls import reverse

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # add additional fields in here

    def __str__(self):
        return self.email
        
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=256, blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to="profile-pictures")

    def has_profile_image(self):
        return self.profile_image != ""

    def has_avatar_url(self):
        return self.avatar_url != ""

    def get_absolute_url(self):
        return reverse('dashboard:profilepic')

    def __str__(self):
        return self.user.email

    class Meta():
        db_table = 'user_profile'