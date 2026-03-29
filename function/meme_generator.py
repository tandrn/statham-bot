import random
import io
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

TEMPLATES_DIR = Path(__file__).parent / "templates"
FONT_PATH = Path(__file__).parent / "impact.ttf"

STATHAM_TEMPLATES = [
    "https://upload.wikimedia.org/wikipedia/commons/d/d3/Jason_Statham_2018.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/50/Jason_Statham_2014.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/39/Jason_Statham_2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1b/Jason_Statham_TIFF%2C_2011.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/2b/Jason-Statham.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/02/Jason_Statham.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/20/Jason_Statham_2007.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/29/Jason_Statham_2012.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/4/4d/Cannes_2014_2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/e/e0/Cannes_2014_3.jpg",
]


def _get_font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(str(FONT_PATH), size)
    except (OSError, IOError):
        pass
    try:
        return ImageFont.truetype("impact.ttf", size)
    except (OSError, IOError):
        pass
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except (OSError, IOError):
        return ImageFont.load_default()


def _draw_text_with_outline(draw: ImageDraw.ImageDraw, text: str, x: int, y: int, font: ImageFont.FreeTypeFont) -> None:
    outline_color = "black"
    text_color = "white"
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
    draw.text((x, y), text, font=font, fill=text_color)


def generate_meme(image_bytes: bytes, quote: str) -> bytes:
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")

    width, height = img.size
    max_width = width - 40

    font_size = max(28, min(60, width // 15))
    font = _get_font(font_size)

    draw = ImageDraw.Draw(img)

    lines = textwrap.wrap(quote, width=30)

    bbox = font.getbbox("Ay")
    line_height = (bbox[3] - bbox[1]) + 10

    total_text_height = len(lines) * line_height
    y_start = height - total_text_height - 30

    for i, line in enumerate(lines):
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = y_start + i * line_height
        _draw_text_with_outline(draw, line, x, y, font)

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=90)
    return output.getvalue()


def get_random_template_url() -> str:
    return random.choice(STATHAM_TEMPLATES)
