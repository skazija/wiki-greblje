import tempfile
from pathlib import Path

import easyocr
from PIL import Image, ImageOps


_reader = None


def get_reader():
    global _reader

    if _reader is None:
        _reader = easyocr.Reader(
            ["bs", "hr", "rs_latin"],
            gpu=False,
        )

    return _reader


def recognize_inscription(image_file):
    image = Image.open(image_file)
    image = ImageOps.exif_transpose(image)
    image = image.convert("RGB")

    reader = get_reader()

    with tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False,
    ) as temp_file:
        temp_path = Path(temp_file.name)

        image.save(
            temp_path,
            format="JPEG",
            quality=95,
        )

    try:
        results = reader.readtext(
            str(temp_path),
            detail=0,
            paragraph=False,
        )

        text = "\n".join(
            line.strip()
            for line in results
            if line and line.strip()
        )

        return text.strip()

    finally:
        temp_path.unlink(missing_ok=True)