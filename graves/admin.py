from django.utils import timezone
from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.geos import Point
from .models import Cemetery, Grave, Person, Photo, EditHistory, LocationSuggestion, EditSuggestion, Comment
from django.db.models import Case, When, Value, IntegerField


class GraveAdminForm(forms.ModelForm):
    latitude = forms.FloatField(required=False, label="Latitude")
    longitude = forms.FloatField(required=False, label="Longitude")

    class Meta:
        model = Grave
        fields = "__all__"
        widgets = {
            "location": forms.HiddenInput(),
        },
        widgets = {"location": forms.HiddenInput(),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cemetery"].queryset = Cemetery.objects.all()

        if self.instance and self.instance.location:
            self.fields["latitude"].initial = self.instance.location.y
            self.fields["longitude"].initial = self.instance.location.x

    def save(self, commit=True):
        obj = super().save(commit=False)

        lat = self.cleaned_data.get("latitude")
        lon = self.cleaned_data.get("longitude")

        if lat is not None and lon is not None:
            obj.location = Point(lon, lat, srid=4326)

        if commit:
            obj.save()
            self.save_m2m()

        return obj


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1

    fields = (
        "image_preview",
        "image",
        "caption",
        "uploaded_by",
        "gps_text",
    )

    readonly_fields = (
        "image_preview",
        "gps_text",
    )

    exclude = ("gps_location",)

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px; max-width:180px; border-radius:6px;" />',
                obj.image.url
            )
        return "-"

    image_preview.short_description = "Preview"

    def gps_text(self, obj):
        if obj and obj.gps_location:
            return f"Lat: {obj.gps_location.y}, Lon: {obj.gps_location.x}"
        return "Nema GPS podataka"

    gps_text.short_description = "GPS"

@admin.register(Cemetery)
class CemeteryAdmin(GISModelAdmin):
    list_display = ("name", "city", "village", "created_at")
    search_fields = ("name", "city", "village")

@admin.register(Grave)
class GraveAdmin(GISModelAdmin):
    form = GraveAdminForm
    actions = ["approve_graves"]
    list_display = (
        "thumbnail",
        "id",
        "title",
        "cemetery",
        "condition",
        "status_badge",
        "latitude_display",
        "longitude_display",
        "created_at",
        "approve_link",
        "edit_link",
        "location_warning",
    )

    search_fields = ("title", "inscription", "notes")
    list_filter = ("cemetery", "condition", "status")
    inlines = [PhotoInline]

    fieldsets = (
        (None, {
            "fields": (
                "cemetery",
                "title",
                "inscription",
                "condition",
                "notes",
                "status",
                "created_by",
            )
        }),
        ("Lokacija", {
            "fields": (
                "latitude",
                "longitude",
            )
        }),
    )

    def latitude_display(self, obj):
        if obj.location:
            return obj.location.y
        return "-"

    latitude_display.short_description = "Latitude"
    
    def approve_link(self, obj):
        if obj.status == Grave.STATUS_PENDING:
            return format_html(
                '<a class="button" href="{}">Odobri</a>',
                f"/admin/graves/grave/{obj.id}/change/"
            )
        return "-"

    approve_link.short_description = "Akcija"
    
    def thumbnail(self, obj):
        first_photo = obj.photos.first()

        if first_photo and first_photo.image:
            return format_html(
                '''
                <a href="{}" target="_blank">
                    <img src="{}"
                        style="height:60px;
                                width:60px;
                                object-fit:cover;
                                border-radius:6px;
                                cursor:zoom-in;" />
                </a>
                ''',
                first_photo.image.url,
                first_photo.image.url
            )

        return "-"

    thumbnail.short_description = "Slika"

    def location_warning(self, obj):
        if not obj.location:
            return "Nema lokacije"

        if not obj.cemetery or not obj.cemetery.boundary:
            return "Nema granice groblja"

        if obj.cemetery.boundary.contains(obj.location):
            return format_html(
                '<span style="color:{};font-weight:bold;">{}</span>',
                "green",
                "OK"
            )

        return format_html(
            '<span style="color:{};font-weight:bold;">{}</span>',
            "red",
            "Van groblja"
        )

    location_warning.short_description = "Lokacija"

    def status_badge(self, obj):
        colors = {
            "approved": "green",
            "pending": "orange",
            "rejected": "red",
        }

        labels = {
            "approved": "ODOBRENO",
            "pending": "PENDING",
            "rejected": "ODBIJENO",
        }

        color = colors.get(obj.status, "gray")
        label = labels.get(obj.status, obj.status)

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            label
        )

    status_badge.short_description = "Status"

    def longitude_display(self, obj):
        if obj.location:
            return obj.location.x
        return "-"

    longitude_display.short_description = "Longitude"

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        return qs.annotate(
            status_priority=Case(
                When(status="pending", then=Value(0)),
                When(status="approved", then=Value(1)),
                When(status="rejected", then=Value(2)),
                default=Value(99),
                output_field=IntegerField(),
            )
        ).order_by("status_priority", "-created_at")

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = Grave.objects.get(pk=obj.pk)

            fields_to_track = [
                "title",
                "inscription",
                "condition",
                "notes",
                "status",
                "location",
                "cemetery",
            ]

            for field in fields_to_track:
                old_value = getattr(old_obj, field)
                new_value = getattr(obj, field)

                if str(old_value) != str(new_value):
                    EditHistory.objects.create(
                        grave=obj,
                        edited_by=request.user,
                        field_name=field,
                        old_value=str(old_value),
                        new_value=str(new_value),
                    )

        super().save_model(request, obj, form, change)

    def edit_link(self, obj):
        return format_html(
            '<a class="button" href="/admin/graves/grave/{}/change/">Uredi</a>',
            obj.id
        )

    edit_link.short_description = "Uredi"


    @admin.action(description="Odobri odabrane grobove")
    def approve_graves(self, request, queryset):
        queryset.update(status=Grave.STATUS_APPROVED)

    class Media:
        css = {
            "all": ("https://unpkg.com/leaflet/dist/leaflet.css",)
        }
        js = (
            "https://unpkg.com/leaflet/dist/leaflet.js",
            "admin/js/grave_location_editor.js",
        )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        cemeteries = Cemetery.objects.exclude(location=None)

        cemetery_locations = {}

        for cemetery in cemeteries:
            cemetery_locations[cemetery.id] = {
                "lat": cemetery.location.y,
                "lng": cemetery.location.x,
            }

        form.cemetery_locations = cemetery_locations

        return form

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "birth_year", "death_year", "grave")
    search_fields = ("first_name", "last_name")


@admin.register(Photo)
class PhotoAdmin(GISModelAdmin):
    list_display = ("id", "grave", "caption", "uploaded_at")


@admin.register(EditHistory)
class EditHistoryAdmin(admin.ModelAdmin):
    list_display = ("grave", "field_name", "edited_by", "edited_at")
    search_fields = ("field_name", "old_value", "new_value")


@admin.register(LocationSuggestion)
class LocationSuggestionAdmin(GISModelAdmin):
    list_display = ("grave", "suggested_by", "approved", "created_at")
    list_filter = ("approved",)



@admin.register(EditSuggestion)
class EditSuggestionAdmin(admin.ModelAdmin):
    actions = ["approve_suggestions"]

    list_display = (
        "grave",
        "field_name",
        "suggested_by",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "field_name",
    )

    search_fields = (
        "grave__title",
        "old_value",
        "new_value",
        "suggested_by__username",
    )

    readonly_fields = (
        "grave",
        "suggested_by",
        "field_name",
        "old_value",
        "new_value",
        "created_at",
    )

    @admin.action(description="Odobri i primijeni prijedloge")
    def approve_suggestions(self, request, queryset):

        for suggestion in queryset:

            if suggestion.status == EditSuggestion.STATUS_APPROVED:
                continue

            grave = suggestion.grave

            setattr(
                grave,
                suggestion.field_name,
                suggestion.new_value
            )

            grave.save()

            suggestion.status = EditSuggestion.STATUS_APPROVED
            suggestion.reviewed_at = timezone.now()

            suggestion.save()

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_obj = EditSuggestion.objects.get(pk=obj.pk)
            old_status = old_obj.status

        super().save_model(request, obj, form, change)

        if (
            obj.status == EditSuggestion.STATUS_APPROVED
            and old_status != EditSuggestion.STATUS_APPROVED
        ):
            grave = obj.grave

            setattr(
                grave,
                obj.field_name,
                obj.new_value
            )

            grave.save()

            EditHistory.objects.create(
                grave=grave,
                edited_by=request.user,
                field_name=obj.field_name,
                old_value=obj.old_value,
                new_value=obj.new_value,
            )
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
    "comment_photo_thumb",
    "grave",
    "author",
    "status",
    "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "grave__title",
        "author__username",
        "text",
    )

    actions = ["approve_comments"]

    def comment_photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '''
                <a href="{}" target="_blank">
                    <img src="{}"
                         style="height:60px;
                                width:60px;
                                object-fit:cover;
                                border-radius:6px;
                                cursor:zoom-in;" />
                </a>
                ''',
                obj.photo.url,
                obj.photo.url
            )

        return "-"

    comment_photo_thumb.short_description = "Slika"

    @admin.action(description="Odobri odabrane komentare")
    def approve_comments(self, request, queryset):
        queryset.update(status=Comment.STATUS_APPROVED)