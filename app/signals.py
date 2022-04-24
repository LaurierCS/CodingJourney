# Imports
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *

# Example: Create a Profile for every new User
def create_profile(sender, instance, created, **kwargs):
    print('user created!!!')
    # if created:
    #     Profile.objects.create(user=instance)

    return None


@receiver(post_save, sender=Profile)
def save_profile(sender, instance, created, **kwargs):
    print('Profile saved!!!')
    print('Sender: ', sender)
    print('Instance', instance)
    print('Created', created)
    return None

@receiver(post_delete, sender=Profile)
def del_profile(sender, instance, **kwargs):
    print('Delete Profile...')


# post_save.connect(save_profile, sender=Profile)
# post_delete.connect(del_profile, sender=Profile)



