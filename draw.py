import tempfile
from PIL import Image, ImageDraw, ImageFont


def generate_image(text, draft: bool, position=None):
    with Image.open('terminal.jpg') as image:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 36)
        draw.text((150, 210), text, font=font)
        if draft and position:
            draw.rectangle(position, outline='red', width=5)

        with tempfile.NamedTemporaryFile(suffix='blk.jpg', delete=False) as temp_file:
            temp_file_path = temp_file.name
            image.save(temp_file_path)

        return temp_file_path
