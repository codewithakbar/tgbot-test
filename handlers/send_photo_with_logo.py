import io
import numpy as np


from PIL import Image, ImageDraw, ImageFilter, ImageOps
import requests
from io import BytesIO

from dispatcher import dp, bot


def test(path, gradient_magnitude=1.):
    im = Image.open(path)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    width, height = im.size
    gradient = Image.new('L', (width, 1), color=0xFF)
    for x in range(width):
        # gradient.putpixel((x, 0), 255-x)
        gradient.putpixel((x, 0), int(255 * (1 - gradient_magnitude * float(x)/width)))
    alpha = gradient.resize(im.size)
    black_im = Image.new('RGBA', (width, height), color=0) # i.e. black
    black_im.putalpha(alpha)
    gradient_im = Image.alpha_composite(im, black_im)
    gradient_im.save('out.png', 'PNG')




async def send_news_with_logo(chat_id, photo_path, news):
    response = requests.get(photo_path)
    response.raise_for_status()
    image_bytes = response.content

    # Загрузка фотографии
    photo = Image.open(io.BytesIO(image_bytes))

    # Загрузка логотипа
    logo_path = "data/sa.png"  # Укажите путь к изображению логотипа
    logo = Image.open(logo_path)

    # Масштабирование логотипа, чтобы он поместился на фотографию
    logo_width, logo_height = logo.size
    max_logo_size = min(photo.width, photo.height) // 2
    if logo_width > max_logo_size or logo_height > max_logo_size:
        logo.thumbnail((max_logo_size, max_logo_size))

    # Расположение логотипа в верхнем правом углу фотографии
    position = (photo.width - logo.width, 0)
    photo.paste(logo, position, logo)

    # Преобразование изображения в байтовый поток
    photo_byte_array = io.BytesIO()
    photo.save(photo_byte_array, format='JPEG')
    photo_byte_array.seek(0)
    # Отправка фотографии с логотипом и заголовком в чат
    await bot.send_photo(chat_id, photo=photo_byte_array, caption=news)
