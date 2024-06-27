import datetime
import os
from django.conf import settings
from rest_framework import viewsets
from PIL import Image
from parser_img.parser_img import download_and_extract, get_images, create_collage, get_direct_link
from .models import File
from .serializers import FileSerializer, DiskUrlSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
@extend_schema(tags=["File"])
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass


@extend_schema(tags=["Parser"])
class DiskUrlViewSet(viewsets.ViewSet):
    serializer_class = DiskUrlSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data, partial=True)
        if serializer.is_valid():
            url = serializer.validated_data["url"]
            name = serializer.validated_data["name"]
            if name:
                name_file = name + '.tif'
            else:
                name_date = datetime.datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S')
                name_file = f"Result_{name_date}.tif"

            try:
                direct_link = get_direct_link(url)
                extract_to = "download"
                download_and_extract(direct_link, extract_to)
                image_paths = get_images(extract_to)

                images = [Image.open(img_path) for img_path in image_paths]
                create_collage(images, name_file)
                print(f"TIFF file created successfully: {name_file}")

                return Response({

                    'message': 'TIFF file created successfully',
                    'file_name': name_file
                    },

                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                print(f"An error occurred: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
