from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
import exifread
from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models


class Cemetery(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    village = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    CEMETERY_TYPE_MUSLIM = "muslimansko"
    CEMETERY_TYPE_CATHOLIC = "katolicko"
    CEMETERY_TYPE_ORTHODOX = "pravoslavno"
    CEMETERY_TYPE_JEWISH = "hebrejsko"
    CEMETERY_TYPE_PARTISAN = "partizansko"
    CEMETERY_TYPE_STECCI = "stecci"
    CEMETERY_TYPE_MILITARY = "vojno"
    CEMETERY_TYPE_CITY = "gradsko"
    CEMETERY_TYPE_VILLAGE = "seosko"
    CEMETERY_TYPE_FAMILY = "porodicno"
    CEMETERY_TYPE_NATURAL = "prirodno"
    CEMETERY_TYPE_MASS_GRAVE = "masovna_grobnica"
    CEMETERY_TYPE_MEMORIAL = "spomen_groblje"
    CEMETERY_TYPE_UNKNOWN = "nepoznato"
    CEMETERY_TYPE_OTHER = "ostalo"

    CEMETERY_TYPE_CHOICES = [
        (CEMETERY_TYPE_MUSLIM, "Muslimansko"),
        (CEMETERY_TYPE_CATHOLIC, "Katoličko"),
        (CEMETERY_TYPE_ORTHODOX, "Pravoslavno"),
        (CEMETERY_TYPE_JEWISH, "Hebrejsko"),
        (CEMETERY_TYPE_PARTISAN, "Partizansko"),
        (CEMETERY_TYPE_STECCI, "Stećci"),
        (CEMETERY_TYPE_MILITARY, "Vojno"),
        (CEMETERY_TYPE_CITY, "Gradsko"),
        (CEMETERY_TYPE_VILLAGE, "Seosko"),
        (CEMETERY_TYPE_FAMILY, "Porodično"),
        (CEMETERY_TYPE_NATURAL, "Prirodno"),
        (CEMETERY_TYPE_MASS_GRAVE, "Masovna grobnica"),
        (CEMETERY_TYPE_MEMORIAL, "Spomen-groblje"),
        (CEMETERY_TYPE_UNKNOWN, "Nepoznato"),
        (CEMETERY_TYPE_OTHER, "Ostalo"),
    ]

    cemetery_type = models.CharField(
        max_length=30,
        choices=CEMETERY_TYPE_CHOICES,
        default=CEMETERY_TYPE_UNKNOWN,
        verbose_name="Vrsta groblja",
    )
    
    location = gis_models.PointField(null=True, blank=True)
    boundary = gis_models.PolygonField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cemeteries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.latitude and self.longitude:
            self.location = Point(
                float(self.longitude),
                float(self.latitude),
                srid=4326
            )
        super().save(*args, **kwargs)
    
    @property
    def primary_photo(self):
        primary = self.photos.filter(
            is_primary=True
        ).first()

        if primary:
            return primary

        return self.photos.first()
    
    @property
    def fallback_icon(self):
        return f"heritage-icons/cemetery/{self.cemetery_type}.png"
    
class CemeteryPhoto(models.Model):
    cemetery = models.ForeignKey(
        Cemetery,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(
        upload_to="cemetery_photos/"
    )

    image_original = models.ImageField(
        upload_to="cemetery_photos/originals/%Y/%m/",
        blank=True,
        null=True,
    )

    caption = models.CharField(
        max_length=255,
        blank=True
    )

    is_primary = models.BooleanField(
        default=False,
        verbose_name="Glavna fotografija"
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        if self.image:
            try:
                # 1. Sačuvaj original netaknut
                if not self.image_original:
                    self.image.seek(0)

                    original_content = ContentFile(
                        self.image.read()
                    )

                    self.image_original.save(
                        self.image.name,
                        original_content,
                        save=False
                    )

                    self.image.seek(0)

                # 2. Napravi optimizovanu web verziju
                img = Image.open(self.image)

                try:
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass

                max_size = (2000, 2000)

                if img.width > 2000 or img.height > 2000:
                    img.thumbnail(
                        max_size,
                        Image.LANCZOS
                    )

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                buffer = BytesIO()

                img.save(
                    buffer,
                    format="JPEG",
                    quality=90,
                    optimize=True
                )

                buffer.seek(0)

                self.image.save(
                    self.image.name,
                    ContentFile(buffer.read()),
                    save=False
                )

            except Exception as e:
                print(
                    f"Cemetery image processing error: {e}"
                )
        # Samo jedna fotografija groblja može biti glavna
        if self.is_primary:
            CemeteryPhoto.objects.filter(
                cemetery=self.cemetery,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Photo for {self.cemetery}"



class Grave(models.Model):
    cemetery = models.ForeignKey(
        Cemetery,
        on_delete=models.CASCADE,
        related_name="graves"
    )

    title = models.CharField(max_length=255, blank=True)
    inscription = models.TextField(blank=True)

    location = gis_models.PointField(null=True, blank=True)

    condition = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: good, damaged, unreadable"
    )

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Čeka odobrenje"),
        (STATUS_APPROVED, "Odobreno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_APPROVED
    )


    notes = models.TextField(blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or f"Grave #{self.id}"

    @property
    def status_order(self):
        order = {
            self.STATUS_PENDING: 0,
            self.STATUS_APPROVED: 1,
            self.STATUS_REJECTED: 2,
        }

        return order.get(self.status, 99)
        
class Person(models.Model):
    GENDER_UNKNOWN = ""
    GENDER_MALE = "male"
    GENDER_FEMALE = "female"

    GENDER_CHOICES = [
        (GENDER_UNKNOWN, "Nije poznato"),
        (GENDER_MALE, "Muško"),
        (GENDER_FEMALE, "Žensko"),
    ]

    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="persons",
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)

    birth_date_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Use if exact date is unclear",
    )

    death_date_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Use if exact date is unclear",
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        default=GENDER_UNKNOWN,
        verbose_name="Spol",
    )

    photo = models.ImageField(
        upload_to="persons/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Fotografija osobe",
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()



class EditHistory(models.Model):
    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="edit_history"
    )

    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)

    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.field_name} changed on {self.grave}"


class LocationSuggestion(models.Model):
    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="location_suggestions"
    )

    suggested_location = gis_models.PointField()
    reason = models.TextField(blank=True)

    suggested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location suggestion for {self.grave}"


class Photo(models.Model):
    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(upload_to="grave_photos/")
    image_original = models.ImageField(upload_to="grave_photos/originals/%Y/%m/", blank=True, null=True,)
    caption = models.CharField(max_length=255, blank=True)

    gps_location = gis_models.PointField(srid=4326, null=True, blank=True)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def _convert_to_degrees(self, value):
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)

    def extract_gps_from_image(self):
        try:
            self.image.open("rb")
            tags = exifread.process_file(self.image.file, details=False)

            lat = tags.get("GPS GPSLatitude")
            lat_ref = tags.get("GPS GPSLatitudeRef")
            lon = tags.get("GPS GPSLongitude")
            lon_ref = tags.get("GPS GPSLongitudeRef")

            if lat and lat_ref and lon and lon_ref:
                latitude = self._convert_to_degrees(lat)
                longitude = self._convert_to_degrees(lon)

                if str(lat_ref) != "N":
                    latitude = -latitude

                if str(lon_ref) != "E":
                    longitude = -longitude

                return Point(longitude, latitude, srid=4326)

        except Exception:
            return None

        return None

    def save(self, *args, **kwargs):

        # GPS iz EXIF-a
        if self.image and not self.gps_location:
            gps_point = self.extract_gps_from_image()
            if gps_point:
                self.gps_location = gps_point

        if self.image:
            try:
                # Ako original još nije sačuvan, sačuvaj upload netaknut
                if not self.image_original:
                    self.image.seek(0)

                    original_content = ContentFile(
                        self.image.read()
                    )

                    self.image_original.save(
                        self.image.name,
                        original_content,
                        save=False
                    )

                    self.image.seek(0)

                # Web verzija
                img = Image.open(self.image)

                try:
                    from PIL import ImageOps
                    img = ImageOps.exif_transpose(img)
                except Exception:
                    pass

                MAX_SIZE = (2000, 2000)

                if img.width > 2000 or img.height > 2000:
                    img.thumbnail(
                        MAX_SIZE,
                        Image.LANCZOS
                    )

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                buffer = BytesIO()

                img.save(
                    buffer,
                    format="JPEG",
                    quality=90,
                    optimize=True
                )

                buffer.seek(0)

                self.image.save(
                    self.image.name,
                    ContentFile(buffer.read()),
                    save=False
                )

            except Exception as e:
                print(f"Image processing error: {e}")
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Photo for {self.grave}"

class EditSuggestion(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Čeka odobrenje"),
        (STATUS_APPROVED, "Odobreno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]

    FIELD_CHOICES = [
        ("title", "Naziv groba"),
        ("inscription", "Natpis"),
        ("condition", "Stanje"),
        ("notes", "Bilješke"),
    ]

    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="edit_suggestions"
    )

    suggested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    field_name = models.CharField(
        max_length=100,
        choices=FIELD_CHOICES
    )

    old_value = models.TextField(blank=True)
    new_value = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    admin_note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.grave} - {self.field_name}"

class Comment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Čeka odobrenje"),
        (STATUS_APPROVED, "Odobreno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]

    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    photo = models.ImageField(
        upload_to="comment_photos/",
        blank=True,
        null=True
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    text = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentar za {self.grave}"


class ProblemReport(models.Model):
    TYPE_LOCATION = "location"
    TYPE_WRONG_CEMETERY = "wrong_cemetery"
    TYPE_DUPLICATE = "duplicate"
    TYPE_PHOTO = "photo"
    TYPE_TEXT = "text"
    TYPE_OTHER = "other"

    TYPE_CHOICES = [
        (TYPE_LOCATION, "Pogrešna lokacija"),
        (TYPE_WRONG_CEMETERY, "Pogrešno groblje"),
        (TYPE_DUPLICATE, "Duplikat"),
        (TYPE_PHOTO, "Problem sa fotografijom"),
        (TYPE_TEXT, "Problem sa tekstom/natpisom"),
        (TYPE_OTHER, "Ostalo"),
    ]

    STATUS_OPEN = "open"
    STATUS_RESOLVED = "resolved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Otvoreno"),
        (STATUS_RESOLVED, "Riješeno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]

    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="problem_reports"
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    problem_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )

    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Problem za {self.grave}"