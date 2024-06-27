import os
import requests
from PIL import Image
import zipfile
import io
import math
from django.conf import settings


def get_direct_link(public_url):
    """Получаем ссылку для скачивания"""
    response = requests.get(settings.API_URL + public_url)
    response.raise_for_status()
    return response.json()['href']


def download_and_extract(direct_link, extract_to):
    """Скачиваем и извлекаем"""
    response = requests.get(direct_link)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_:
        zip_.extractall(extract_to)


def get_images(directory):
    """Забираем изображения"""
    images = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                images.append(os.path.join(root, file))
    return images


def create_collage(images, output_file, image_size=None, margin=None):
    """Создаем коллаж"""
    if not images:
        raise ValueError("No images found.")

    if image_size:
        resized_images = [img.resize(image_size) for img in images]
    else:
        resized_images = images

    # Получаем максимальные ширину и высоту изображений
    image_width = max(img.width for img in resized_images)
    image_height = max(img.height for img in resized_images)

    images_per_row = 7  # количество изображений в ряду

    total_width = images_per_row * (image_width + margin) + margin
    collage_height = math.ceil(len(resized_images) / images_per_row) * (image_height + margin) + margin

    # Создаем фоновое изображение
    collage_image = Image.new('RGBA', (total_width, collage_height), (255, 255, 255, 255))
    x_offset, y_offset = margin, margin

    for i, img in enumerate(resized_images):
        row = i // images_per_row  # вычисляем ряд
        col = i % images_per_row  # вычисляем столбец

        offset_x = (image_width - img.width) // 2
        offset_y = (image_height - img.height) // 2

        paste_x = x_offset + col * (image_width + margin) + offset_x
        paste_y = y_offset + row * (image_height + margin) + offset_y

        collage_image.paste(img, (paste_x, paste_y))

    save_kwargs = {"compression": "jpeg"}  # Устанавливаем компрессию изображений

    output_file_path = os.path.join(settings.MEDIA_ROOT, "image", output_file)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    collage_image.save(output_file_path, **save_kwargs)
    file = f"image/{output_file}"

    return file

