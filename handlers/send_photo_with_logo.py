import io
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import requests
from io import BytesIO
from dispatcher import dp, bot

from keyboards.inline.admin import confirmation_keyboard



def test(path, gradient_magnitude=1.):
    im = Image.open(path)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    width, height = im.size
    gradient = Image.new('L', (width, 1), color=0xFF)
    for x in range(width):
        gradient.putpixel((x, 0), int(255 * (1 - gradient_magnitude * float(x) / width)))
    alpha = gradient.resize(im.size)
    black_im = Image.new('RGBA', (width, height), color=0)
    black_im.putalpha(alpha)
    gradient_im = Image.alpha_composite(im, black_im)
    gradient_im.save('out.png', 'PNG')


async def send_news_with_logo(chat_id, photo_path, news):
    response = requests.get(photo_path)
    response.raise_for_status()
    image_bytes = response.content

    # Load the photo
    photo = Image.open(io.BytesIO(image_bytes))

    # Load the logo
    logo_path = "data/sa.png"  # Specify the path to the logo image
    logo = Image.open(logo_path)

    # Scale the logo to fit within the photo
    logo_width, logo_height = logo.size
    max_logo_size = min(photo.width, photo.height) // 2
    if logo_width > max_logo_size or logo_height > max_logo_size:
        logo.thumbnail((max_logo_size, max_logo_size))

    # Position the logo in the top-right corner of the photo
    position = (photo.width - logo.width, 0)
    photo.paste(logo, position, logo)

    # Convert the image mode from RGBA to RGB
    photo = photo.convert('RGB')

    # Convert the image to a byte stream
    photo_byte_array = io.BytesIO()
    photo.save(photo_byte_array, format='JPEG')
    photo_byte_array.seek(0)

    # Send the photo with the logo and caption to the chat
    await bot.send_photo(chat_id, photo=photo_byte_array, caption=news, reply_markup=confirmation_keyboard)
