import os
import sys
from io import BytesIO

from PIL import Image, ImageDraw
from PIL.ImageFont import truetype
from django.core.files.uploadedfile import InMemoryUploadedFile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = os.path.join(HERE, "watermark-font.ttf")


font_size = 18

watermark_font = truetype(FONT_PATH, font_size)


def add_watermark(image, text, font=watermark_font) -> Image:
    """
    Add a watermark to the pin.
    :param image: Source image file
    :type image : :class:`PIL.Image`
    :param text: The text of watermark
    :type text: String
    :param font: font type
    :type font: font
    :return: Image with watermark
    :rtype: class:`PIL.Image`
    """
    rgba_image = image.convert('RGBA')
    text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)

    text_size_x, text_size_y = image_draw.textsize(text, font=font)

    # Set text position.
    text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)

    # Set text color and transparency.
    image_draw.text(text_xy, text, font=font, fill=(128, 128, 128, 180))
    image_with_watermark = Image.alpha_composite(rgba_image, text_overlay)
    return image_with_watermark


from core.models import Image as PinImage


def get_new_image_field(image_in):
    image_file = Image.open(image_in.file)
    handled_image = add_watermark(image_file, "hello watermark")
    if handled_image.mode in ("RGBA", "P"):
        handled_image = handled_image.convert("RGB")
    output = BytesIO()
    handled_image.save(output, format='JPEG', quality=100)
    output.seek(0)
    image_field = InMemoryUploadedFile(
        file=output,
        field_name="image",
        name=image_in.name,
        content_type=None,
        size=image_in.tell(),
        charset=None,
    )
    return image_field


class Plugin:
    def process_image_pre_creation(self, django_settings, image_instance: PinImage):
        image_instance.image = get_new_image_field(image_instance.image.file)

    def process_thumbnail_pre_creation(self, django_settings, thumbnail_instance):
        thumbnail_instance.image = get_new_image_field(thumbnail_instance.image)
