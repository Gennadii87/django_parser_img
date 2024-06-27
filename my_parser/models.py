from django.db import models
from django.utils import timezone


class File(models.Model):
    objects = None

    name = models.CharField(max_length=255)
    data_creation = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='image/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.file}"
