from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from .models import UserProfile

@receiver(user_signed_up)
def social_login_set_profilepic(request, sociallogin, user, **kwargs):
    if sociallogin.account.provider == 'google':
        picture_url = sociallogin.account.extra_data['picture']
        profile = UserProfile(user=user, avatar_url=picture_url)
        profile.save()
