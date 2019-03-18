from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_signed_up)
def social_login_set_profilepic(sender, **kwargs):
    user = kwargs['user']
    profile = UserProfile(user=user, avatar_url="testing...")
    profile.save()
