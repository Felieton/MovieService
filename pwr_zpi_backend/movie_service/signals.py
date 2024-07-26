from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import Group
from .models import User, UserSettings


@receiver(post_save, sender=User, dispatch_uid='on_create_user_post')
def on_create_user_post(sender, instance: User, created, **kwargs):
    if created:
        # should not happen but let's check it anyway
        if instance.settings is None:
            # create default settings for new user
            instance.settings = UserSettings()
            instance.settings.save()
            instance.save()
        if instance.groups.count() == 0:
            group_name = 'Administrator' if instance.is_superuser else 'User'
            group = Group.objects.get(name=group_name)
            instance.groups.add(group)
