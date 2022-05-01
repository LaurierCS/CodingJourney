# Imports
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

# Example: Create a Profile for every new User
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
        )

@receiver(post_delete, sender=Profile)
def del_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()


