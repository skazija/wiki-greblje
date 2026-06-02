import exifread

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.geos import Point

from .models import Photo, LocationSuggestion


def convert_to_degrees(value):
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)
    return d + (m / 60.0) + (s / 3600.0)


def extract_gps(image_path):
    try:
        with open(image_path, "rb") as image_file:
            tags = exifread.process_file(image_file, details=False)

        lat = tags.get("GPS GPSLatitude")
        lat_ref = tags.get("GPS GPSLatitudeRef")
        lon = tags.get("GPS GPSLongitude")
        lon_ref = tags.get("GPS GPSLongitudeRef")

        if not all([lat, lat_ref, lon, lon_ref]):
            return None

        latitude = convert_to_degrees(lat)
        longitude = convert_to_degrees(lon)

        if str(lat_ref) != "N":
            latitude = -latitude

        if str(lon_ref) != "E":
            longitude = -longitude

        return Point(longitude, latitude, srid=4326)

    except Exception as e:
        print("EXIF GPS error:", e)
        return None


@receiver(post_save, sender=Photo)
def photo_extract_gps(sender, instance, created, **kwargs):
    if not instance.image:
        return

    gps_point = instance.gps_location

    if not gps_point:
        gps_point = extract_gps(instance.image.path)

    if not gps_point:
        print("Nema GPS podataka u fotografiji:", instance.image.path)
        return

    if not instance.gps_location:
        Photo.objects.filter(id=instance.id).update(gps_location=gps_point)

    grave = instance.grave

    if not grave.location:
        grave.location = gps_point
        grave.save(update_fields=["location"])

    if created:
        LocationSuggestion.objects.create(
            grave=grave,
            suggested_location=gps_point,
            reason="Lokacija automatski preuzeta iz EXIF GPS podataka fotografije.",
            suggested_by=instance.uploaded_by,
        )