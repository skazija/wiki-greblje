from PIL import Image, ImageOps
from io import BytesIO
from django.core.files.base import ContentFile
import exifread
from django.contrib.gis.geos import Point
from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from graves.services.image_processing import (create_archival_image, create_web_image,)


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
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Čeka odobrenje"),
        (STATUS_APPROVED, "Odobreno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_APPROVED,
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
                # 1. Sačuvaj original 
                if not self.image_original:
                    archival_image = create_archival_image(
                        self.image,
                        max_size=(4000, 4000),
                        quality=88,
                    )

                    archival_content = ContentFile(
                        archival_image.getvalue(),
                        name=self.image.name,
                    )

                    self.image_original.save(
                        self.image.name,
                        archival_content,
                        save=False,
                    )

                # 2. Napravi optimizovanu web verziju
                web_image = create_web_image(self.image)

                web_content = ContentFile(
                    web_image.getvalue(),
                    name=self.image.name,
                )

                self.image.save(
                    self.image.name,
                    web_content,
                    save=False,
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



# ============================================================
# WIKI GREBLJE - SIFRARNIK TIPOVA SPOMENIKA V1.0
# ============================================================


class MonumentMacroType(models.Model):
    """
    Najvisi nivo klasifikacije spomenika.
    Primjeri: nadgrobnik, grobnica/funerarna arhitektura, memorijal.
    """

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Naziv",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivan",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Makro-tip spomenika"
        verbose_name_plural = "Makro-tipovi spomenika"

    def __str__(self):
        return f"{self.code} - {self.name}"


class MonumentTradition(models.Model):
    """
    Tradicija ili historijski/kulturni kontekst spomenika.
    Ne predstavlja fizicki oblik spomenika.
    """

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Naziv",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivna",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Tradicija spomenika"
        verbose_name_plural = "Tradicije spomenika"

    def __str__(self):
        return f"{self.code} - {self.name}"


class MonumentType(models.Model):
    """
    Hijerarhijski sifrarnik fizickih i morfoloskih tipova.

    Primjer:
        Nisan
          -> Nisan sa turbanom
               -> Aginski turban

    Parent omogucava proizvoljnu dubinu bez promjene strukture baze.
    """

    LEVEL_PHYSICAL = "physical"
    LEVEL_MORPHOLOGICAL = "morphological"
    LEVEL_DETAILED = "detailed"
    LEVEL_FUNCTIONAL = "functional"
    LEVEL_LOCAL = "local"
    LEVEL_RESERVE = "reserve"
    LEVEL_EXPERT = "expert"

    LEVEL_CHOICES = [
        (LEVEL_PHYSICAL, "Fizički tip"),
        (LEVEL_MORPHOLOGICAL, "Morfološki podtip"),
        (LEVEL_DETAILED, "Detaljni morfološki podtip"),
        (LEVEL_FUNCTIONAL, "Funkcionalni tip"),
        (LEVEL_LOCAL, "Detaljni / lokalni tip"),
        (LEVEL_RESERVE, "Rezervni kod"),
        (LEVEL_EXPERT, "Funkcionalna / stručna oznaka"),
    ]

    code = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Naziv",
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Nadređeni tip",
    )

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default=LEVEL_PHYSICAL,
        verbose_name="Nivo klasifikacije",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    identification_notes = models.TextField(
        blank=True,
        verbose_name="Kako prepoznati",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivan",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Tip spomenika"
        verbose_name_plural = "Tipovi spomenika"

    @property
    def full_path(self):
        parts = [self.name]
        parent = self.parent

        while parent:
            parts.insert(0, parent.name)
            parent = parent.parent

        return " → ".join(parts)
    
    def __str__(self):
        return f"{self.code} - {self.full_path}"


class Motif(models.Model):
    """
    Sifrarnik ornamentike, simbola i vidljivih motiva.

    Motiv opisuje ono sto je evidentirano na spomeniku.
    Interpretacija znacenja motiva nije dio ovog modela.
    """

    code = models.CharField(
        max_length=40,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Naziv",
    )

    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Kategorija",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivan",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Motiv / ornament"
        verbose_name_plural = "Motivi / ornamenti"

    def __str__(self):
        return f"{self.code} - {self.name}"
    
# ============================================================
# WIKI GREBLJE - STANJE I DEGRADACIJA SPOMENIKA V1.0
# ============================================================


class MonumentCondition(models.Model):
    """
    Opća ocjena stanja očuvanosti spomenika.

    Ovo je praktična Wiki Greblje klasifikacija, a ne
    detaljna konzervatorska dijagnoza.
    """

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Naziv",
    )

    public_label = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Naziv za javni unos",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivno",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Stanje spomenika"
        verbose_name_plural = "Stanja spomenika"

    def __str__(self):
        return f"{self.code} - {self.name}"


class DeteriorationPattern(models.Model):
    """
    Kontrolisani šifrarnik vidljivih pojava degradacije.

    Stručni nivo može pratiti ICOMOS-ISCS terminologiju,
    dok admin_label i public_label omogućavaju jednostavniji
    prikaz bez izlaganja korisnika stručnoj terminologiji.
    """

    GROUP_CRACK = "crack"
    GROUP_DETACHMENT = "detachment"
    GROUP_LOSS = "loss"
    GROUP_DISCOLORATION = "discoloration"
    GROUP_BIOLOGICAL = "biological"

    GROUP_CHOICES = [
        (GROUP_CRACK, "Pukotine i deformacije"),
        (GROUP_DETACHMENT, "Odvajanje materijala"),
        (GROUP_LOSS, "Gubitak materijala"),
        (GROUP_DISCOLORATION, "Promjene boje i naslage"),
        (GROUP_BIOLOGICAL, "Biološka kolonizacija"),
    ]

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Stručni naziv",
    )

    group = models.CharField(
        max_length=20,
        choices=GROUP_CHOICES,
        verbose_name="Grupa",
    )

    admin_label = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Prikaz administratoru",
    )

    public_label = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Prikaz korisniku",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivno",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Pojava degradacije"
        verbose_name_plural = "Pojave degradacije"

    def __str__(self):
        return f"{self.code} - {self.name}"


class MonumentPosition(models.Model):
    """
    Položaj spomenika evidentira se odvojeno od njegovog
    fizičkog stanja i pojava degradacije.
    """

    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Kod",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Naziv",
    )

    public_label = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Naziv za javni unos",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Opis",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Aktivno",
    )

    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Redoslijed",
    )

    class Meta:
        ordering = ["sort_order", "code"]
        verbose_name = "Položaj spomenika"
        verbose_name_plural = "Položaji spomenika"

    def __str__(self):
        return f"{self.code} - {self.name}"

class Grave(models.Model):
    cemetery = models.ForeignKey(
        Cemetery,
        on_delete=models.CASCADE,
        related_name="graves"
    )

    # ========================================================
    # KLASIFIKACIJA SPOMENIKA - WIKI GREBLJE STANDARD V1.0
    # ========================================================

    macro_type = models.ForeignKey(
        MonumentMacroType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="graves",
        verbose_name="Makro-tip",
    )

    tradition = models.ForeignKey(
        MonumentTradition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="graves",
        verbose_name="Tradicija / kontekst",
    )

    monument_type = models.ForeignKey(
        MonumentType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="graves",
        verbose_name="Tip spomenika",
    )

    motifs = models.ManyToManyField(
        Motif,
        blank=True,
        related_name="graves",
        verbose_name="Motivi / ornamentika",
    )
    
    title = models.CharField(max_length=255, blank=True)
    inscription = models.TextField(blank=True)

    location = gis_models.PointField(null=True, blank=True)

    condition = models.CharField(
        max_length=100,
        blank=True,
        help_text="Example: good, damaged, unreadable"
    )

    # ========================================================
    # STANJE SPOMENIKA - WIKI GREBLJE CONDITION STANDARD V1.0
    # ========================================================

    condition_classification = models.ForeignKey(
        MonumentCondition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="graves",
        verbose_name="Opće stanje spomenika",
    )

    deterioration_patterns = models.ManyToManyField(
        DeteriorationPattern,
        blank=True,
        related_name="graves",
        verbose_name="Uočene pojave degradacije",
    )

    monument_position = models.ForeignKey(
        MonumentPosition,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="graves",
        verbose_name="Položaj spomenika",
    )

    condition_notes = models.TextField(
        blank=True,
        verbose_name="Opis stanja",
        help_text=(
            "Kratak opis vidljivog stanja, oštećenja i drugih "
            "zapažanja koja nisu dovoljno obuhvaćena šifrarnikom."
        ),
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
    
    @property
    def primary_photo(self):
        primary = self.photos.filter(
            is_primary=True
        ).first()

        if primary:
            return primary

        return self.photos.first()

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
        related_name="persons",
    )

    first_name = models.CharField(
        max_length=100,
        blank=True,
    )
    last_name = models.CharField(max_length=100, blank=True)
    is_unknown = models.BooleanField(
        default=False,
        verbose_name="Nepoznata osoba",
    )
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

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_APPROVED,
        verbose_name="Status",
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_persons",
        verbose_name="Dodao korisnik",
    )
    
    photo = models.ImageField(
        upload_to="persons/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Fotografija osobe",
    )
    
    photo_original = models.ImageField(
        upload_to="persons/originals/%Y/%m/",
        blank=True,
        null=True,
        verbose_name="Arhivska fotografija osobe",
    )

    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.photo:
            try:
                # Arhivska verzija
                if not self.photo_original:
                    archival_image = create_archival_image(
                        self.photo,
                        max_size=(4000, 4000),
                        quality=88,
                    )

                    archival_content = ContentFile(
                        archival_image.getvalue(),
                        name=self.photo.name,
                    )

                    self.photo_original.save(
                        self.photo.name,
                        archival_content,
                        save=False,
                    )

                # Web verzija
                web_image = create_web_image(
                    self.photo,
                    max_size=(2000, 2000),
                    quality=90,
                )

                web_content = ContentFile(
                    web_image.getvalue(),
                    name=self.photo.name,
                )

                self.photo.save(
                    self.photo.name,
                    web_content,
                    save=False,
                )

            except Exception as e:
                print(f"Person image processing error: {e}")

        super().save(*args, **kwargs)
    
    def __str__(self):
        if self.is_unknown:
            return "Nepoznata osoba"

        full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()

        if full_name:
            return full_name

        return "Nepoznata osoba"

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

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Čeka odobrenje"),
        (STATUS_APPROVED, "Odobreno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]

    image = models.ImageField(upload_to="grave_photos/")
    image_original = models.ImageField(upload_to="grave_photos/originals/%Y/%m/", blank=True, null=True,)
    caption = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPROVED,)
    
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Glavna fotografija"
    )
    
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
                if not self.image_original:
                    archival_image = create_archival_image(
                        self.image,
                        max_size=(4000, 4000),
                        quality=88,
                    )

                    archival_content = ContentFile(
                        archival_image.getvalue(),
                        name=self.image.name,
                    )

                    self.image_original.save(
                        self.image.name,
                        archival_content,
                        save=False,
                    )

                web_image = create_web_image(self.image)

                web_content = ContentFile(
                    web_image.getvalue(),
                    name=self.image.name,
                )

                self.image.save(
                    self.image.name,
                    web_content,
                    save=False,
                )

            except Exception as e:
                print(f"Image processing error: {e}")
        
        # Samo jedna fotografija groba može biti glavna
        if self.is_primary:
            Photo.objects.filter(
                grave=self.grave,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)        
                
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
    
class PersonEditSuggestion(models.Model):

    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Čeka odobrenje"),
        (STATUS_APPROVED, "Odobreno"),
        (STATUS_REJECTED, "Odbijeno"),
    ]

    FIELD_CHOICES = [
        ("first_name", "Ime"),
        ("last_name", "Prezime"),
        ("birth_year", "Godina rođenja"),
        ("death_year", "Godina smrti"),
        ("gender", "Spol"),
        ("notes", "Bilješke o osobi"),
    ]

    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="edit_suggestions",
    )

    suggested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    field_name = models.CharField(
        max_length=100,
        choices=FIELD_CHOICES,
    )

    old_value = models.TextField(
        blank=True,
    )

    new_value = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    admin_note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.person} - {self.field_name}"

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

    def save(self, *args, **kwargs):
        if self.photo:
            try:
                web_image = create_web_image(
                    self.photo,
                    max_size=(2000, 2000),
                    quality=90,
                )

                web_content = ContentFile(
                    web_image.getvalue(),
                    name=self.photo.name,
                )

                self.photo.save(
                    self.photo.name,
                    web_content,
                    save=False,
                )

            except Exception as e:
                print(f"Comment image processing error: {e}")

        super().save(*args, **kwargs)

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