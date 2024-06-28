import datetime
import shutil
from PIL import Image

from parser_img.parser_img import download_and_extract, get_images, create_collage, get_direct_link
from .models import File
from .serializers import FileSerializer, DiskUrlSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema


@extend_schema(tags=["File"])
class FileViewSet(viewsets.ViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def list(self, request, *args, **kwargs):
        model = self.queryset.all()
        result = self.serializer_class(model, many=True, context={'request': request})
        return Response(result.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        file_id = kwargs.get("pk")
        try:
            model = self.queryset.filter(id=file_id)
            if model:
                result = self.serializer_class(model.first(), context={'request': request})

                return Response(result.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        file_id = kwargs.get("pk")
        try:
            models = self.queryset.filter(id=file_id)

            if models:
                model = models.first()
                file_name = model.name
                model.delete()

                return Response({
                    "id": file_id,
                    "name": file_name,
                    "message": "object is delete"
                },
                    status=status.HTTP_200_OK
                )
            else:
                return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Parser"])
class DiskUrlViewSet(viewsets.ViewSet):
    serializer_class = DiskUrlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)

        width = serializer.initial_data.get("width")
        height = serializer.initial_data.get("height")
        margin = int(serializer.initial_data.get("margin") or 1)
        img_row = int(serializer.initial_data.get("img_row") or 1)

        if not width or not height:
            image_size = None
        else:
            image_size = (int(width), int(height))

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
                result = create_collage(images, name_file, image_size, margin, img_row)

                shutil.rmtree("download")

                file_model = File(
                    name=name_file,
                    file=result
                )
                file_model.save()

                file_url = request.build_absolute_uri(file_model.file.url)

                return Response({

                    "message": "TIFF file created successfully",
                    "file": file_url
                },

                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                print(f"An error occurred: {e}")
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
