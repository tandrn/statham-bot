import random
import io
import logging
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

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
    font_paths = [
        str(FONT_PATH),
        "impact.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    ]
    for path in font_paths:
        try:
            font = ImageFont.truetype(path, size)
            logger.info("Loaded font: %s (size %d)", path, size)
            return font
        except (OSError, IOError):
            continue
    logger.warning("No TTF font found, using default")
    return ImageFont.load_default()


def _draw_text_with_outline(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
    outline_width: int = 3,
) -> None:
    for dx in range(-outline_width, outline_width + 1):
        for dy in range(-outline_width, outline_width + 1):
            if dx * dx + dy * dy <= outline_width * outline_width + 1:
                draw.text((x + dx, y + dy), text, font=font, fill="black")
    draw.text((x, y), text, font=font, fill="white")


def generate_meme(image_bytes: bytes, quote: str) -> bytes:
    logger.info("Generating meme with quote: %s", quote[:50])
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")

    width, height = img.size
    logger.info("Image size: %dx%d", width, height)

    font_size = max(24, min(56, width // 12))
    font = _get_font(font_size)

    draw = ImageDraw.Draw(img)

    max_chars = max(15, width // 20)
    lines = textwrap.wrap(quote, width=max_chars)

    try:
        bbox = font.getbbox("Ay")
        line_height = (bbox[3] - bbox[1]) + 12
    except Exception:
        line_height = font_size + 12

    total_text_height = len(lines) * line_height
    y_start = height - total_text_height - 25

    for i, line in enumerate(lines):
        try:
            bbox = font.getbbox(line)
            text_width = bbox[2] - bbox[0]
        except Exception:
            text_width = len(line) * font_size // 2

        x = max(10, (width - text_width) // 2)
        y = y_start + i * line_height

        _draw_text_with_outline(draw, line, x, y, font, outline_width=3)

    output = io.BytesIO()
    img.save(output, format="JPEG", quality=90)
    result = output.getvalue()
    logger.info("Meme generated: %d bytes", len(result))
    return result


def get_random_template_url() -> str:
    return random.choice(STATHAM_TEMPLATES)
