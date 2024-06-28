from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
from .models import File


@receiver(post_delete, sender=File)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
