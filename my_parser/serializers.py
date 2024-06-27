from rest_framework import serializers
from django.core.validators import MaxLengthValidator, MinLengthValidator, MinValueValidator, MaxValueValidator

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
    width = serializers.IntegerField(
        help_text="Ширина",
        required=False,
        default=500,
        validators=[MinValueValidator(10), MaxValueValidator(1000)],
    )
    height = serializers.IntegerField(
        help_text="Высота",
        required=False,
        default=500,
        validators=[MinValueValidator(10), MaxValueValidator(1000)],
    )
    margin = serializers.IntegerField(
        help_text="Отступ",
        required=False,
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(200)],
    )
