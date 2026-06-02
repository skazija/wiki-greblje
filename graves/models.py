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

    location = gis_models.PointField(null=True, blank=True)
    boundary = gis_models.PolygonField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Cemeteries"

    def __str__(self):
        return self.name


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
    grave = models.ForeignKey(
        Grave,
        on_delete=models.CASCADE,
        related_name="persons"
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)

    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)

    birth_date_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Use if exact date is unclear"
    )

    death_date_text = models.CharField(
        max_length=100,
        blank=True,
        help_text="Use if exact date is unclear"
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
        if self.image and not self.gps_location:
            gps_point = self.extract_gps_from_image()
            if gps_point:
                self.gps_location = gps_point

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