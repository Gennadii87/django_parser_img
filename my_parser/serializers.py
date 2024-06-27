from rest_framework import serializers
from django.core.validators import MaxLengthValidator, MinLengthValidator


from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'


class DiskUrlSerializer(serializers.Serializer, metaclass=serializers.SerializerMetaclass):
    url = serializers.URLField(help_text="URL YANDEX DISK", required=True)
    name = serializers.CharField(
        help_text="Название файла",
        required=False,
        allow_blank=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(25)],
    )