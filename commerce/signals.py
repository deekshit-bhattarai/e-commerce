from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal Handler to create new user automatically once a user is created
    """

    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, created, **kwargs):
    """
    Signal to handle saving of user in UserProfile when User is saved 
    """
    try: 
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        pass
