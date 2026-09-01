from io import BytesIO

from PIL import Image, ImageOps


def create_web_image(
    image_file,
    max_size=(2000, 2000),
    quality=90,
):
    """
    Kreira optimizovanu JPEG verziju fotografije za web.

    Originalni upload se ne mijenja.
    EXIF/GPS podatke treba izdvojiti prije poziva ove funkcije.
    """

    image_file.seek(0)

    image = Image.open(image_file)

    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    if image.width > max_size[0] or image.height > max_size[1]:
        image.thumbnail(
            max_size,
            Image.LANCZOS,
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True,
    )

    buffer.seek(0)

    return buffer

def create_archival_image(
    image_file,
    max_size=(4000, 4000),
    quality=88,
):
    """
    Kreira arhivsku JPEG verziju fotografije.

    Namijenjena je za dugoročno čuvanje kvalitetnije verzije slike,
    bez zadržavanja nepotrebno velikih originalnih uploadova.

    EXIF/GPS podatke treba izdvojiti prije poziva ove funkcije.
    """

    image_file.seek(0)

    image = Image.open(image_file)

    try:
        image = ImageOps.exif_transpose(image)
    except Exception:
        pass

    if image.width > max_size[0] or image.height > max_size[1]:
        image.thumbnail(
            max_size,
            Image.LANCZOS,
        )

    if image.mode != "RGB":
        image = image.convert("RGB")

    buffer = BytesIO()

    image.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True,
    )

    buffer.seek(0)

    return buffer