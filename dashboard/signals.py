from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_signed_up)
def social_login_set_profilepic(sender, **kwargs):
    if 'sociallogin' in kwargs and 'user' in kwargs and kwargs['sociallogin'].account.provider == 'google':
        picture_url = kwargs['sociallogin'].account.extra_data['picture']
        profile = UserProfile(user=kwargs['user'], avatar_url=picture_url)
        profile.save()
