from django.utils import timezone
from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.geos import Point
from .models import Cemetery, Grave, Person, Photo, EditHistory, LocationSuggestion, EditSuggestion, Comment, ProblemReport, CemeteryPhoto
from django.db.models import Case, When, Value, IntegerField
import json
from django.contrib.gis.geos import Polygon
from django.shortcuts import redirect
from django.urls import path

class CemeteryAdminForm(forms.ModelForm):

    boundary_geojson = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    
    
    class Meta:
        model = Cemetery
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.location:
            self.fields["latitude"].initial = self.instance.location.y
            self.fields["longitude"].initial = self.instance.location.x


    class Media:
        css = {
            "all": (
                "https://unpkg.com/leaflet/dist/leaflet.css",
            )
        }

        js = (
            "https://unpkg.com/leaflet/dist/leaflet.js",
            "admin/js/cemetery_location_editor.js",
        )

    boundary_geojson = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    def save(self, commit=True):
        cemetery = super().save(commit=False)

        boundary_data = self.cleaned_data.get("boundary_geojson")

        if boundary_data:
            coords = json.loads(boundary_data)

            if len(coords) >= 3:
                points = [(float(lng), float(lat)) for lat, lng in coords]

                if points[0] != points[-1]:
                    points.append(points[0])

                cemetery.boundary = Polygon(points, srid=4326)

        if commit:
            cemetery.save()

        return cemetery

class GraveAdminForm(forms.ModelForm):
    latitude = forms.FloatField(required=False, label="Latitude")
    longitude = forms.FloatField(required=False, label="Longitude")

    class Meta:
        model = Grave
        fields = "__all__"
       
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
        "is_primary",
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

class CemeteryPhotoInline(admin.TabularInline):
    model = CemeteryPhoto
    extra = 1

    fields = (
        "image_preview",
        "image",
        "caption",
        "is_primary",
    )

    readonly_fields = (
        "image_preview",
    )

    def image_preview(self, obj):
        if obj and obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" '
                'style="height:90px; width:120px; '
                'object-fit:cover; border-radius:6px;" />'
                '</a>',
                obj.image.url,
                obj.image.url,
            )

        return "-"

    image_preview.short_description = "Pregled"


@admin.register(Cemetery)
class CemeteryAdmin(admin.ModelAdmin):
    form = CemeteryAdminForm
    inlines = [CemeteryPhotoInline]
    
    fieldsets = (
        ("Osnovni podaci", {
            "fields": (
                "name",
                "cemetery_type",
                "city",
                "village",
                "description",
                "latitude",
                "longitude",
                "boundary_geojson",
            )
        }),

    )
    list_display = ("name", "cemetery_type", "city", "village", "created_at")
    search_fields = ("name", "city", "village")
    list_filter = ("cemetery_type",)
    
class PersonInline(admin.StackedInline):
    model = Person
    extra = 0

    fields = (
        "first_name",
        "last_name",
        "birth_year",
        "death_year",
        "gender",
        "photo",
        "notes",
    )

    
    @admin.display(boolean=True, description="Fotografija")
    def has_photo(self, obj):
        return bool(obj.photo)

    @admin.display(description="Pregled fotografije")
    def photo_preview(self, obj):
        if obj and obj.photo:
            return format_html(
                '<img src="{}" style="max-width:180px; '
                'max-height:240px; object-fit:cover; border-radius:8px;" />',
                obj.photo.url,
            )

        return "Fotografija nije dodana"

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
    inlines = [PersonInline, PhotoInline]

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

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:grave_id>/approve/",
                self.admin_site.admin_view(self.approve_grave),
                name="graves_grave_approve",
            ),
        ]

        return custom_urls + urls


    def approve_grave(self, request, grave_id):
        grave = Grave.objects.get(id=grave_id)
        grave.status = Grave.STATUS_APPROVED
        grave.save()

        return redirect("/admin/graves/grave/")


    def latitude_display(self, obj):
        if obj.location:
            return obj.location.y
        return "-"

    latitude_display.short_description = "Latitude"
    
    def approve_link(self, obj):
        if obj.status == Grave.STATUS_PENDING:
            return format_html(
                '<a class="button" href="{}">Odobri odmah</a>',
                f"/admin/graves/grave/{obj.id}/approve/"
            )
        return "-"

    approve_link.short_description = "Akcija"
    
    def thumbnail(self, obj):
        photo = obj.primary_photo

        if photo and photo.image:
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
                photo.image.url,
                photo.image.url
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
        labels = {
            "approved": "ODOBRENO",
            "pending": "PENDING",
            "rejected": "ODBIJENO",
        }

        label = labels.get(obj.status, obj.status)

        status_class = {
            "approved": "wg-status-approved",
            "pending": "wg-status-pending",
            "rejected": "wg-status-rejected",
        }.get(obj.status, "")

        return format_html(
            '<span class="wg-status {}">{}</span>',
            status_class,
            label,
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

    actions = ["approve_persons", "reject_persons"]

    list_display = (
        "first_name",
        "last_name",
        "grave",
        "gender",
        "birth_year",
        "death_year",
        "status_badge",
        "created_by",
        "approve_link",
    )

    list_filter = (
        "status",
        "gender",
        "is_unknown",
    )

    search_fields = (
        "first_name",
        "last_name",
        "grave__title",
        "created_by__username",
    )

    fields = (
        "grave",
        "is_unknown",
        "first_name",
        "last_name",
        "birth_year",
        "death_year",
        "birth_date_text",
        "death_date_text",
        "gender",
        "photo",
        "notes",
        "status",
        "created_by",
    )

    def status_badge(self, obj):
        labels = {
            Person.STATUS_APPROVED: "ODOBRENO",
            Person.STATUS_PENDING: "PENDING",
            Person.STATUS_REJECTED: "ODBIJENO",
        }

        status_class = {
            Person.STATUS_APPROVED: "wg-status-approved",
            Person.STATUS_PENDING: "wg-status-pending",
            Person.STATUS_REJECTED: "wg-status-rejected",
        }.get(obj.status, "")

        return format_html(
            '<span class="wg-status {}">{}</span>',
            status_class,
            labels.get(obj.status, obj.status),
        )

    status_badge.short_description = "Status"

    def approve_link(self, obj):
        if obj.status == Person.STATUS_PENDING:
            return format_html(
                '<a class="button" href="{}">Odobri</a>',
                f"/admin/graves/person/{obj.id}/approve/"
            )

        return "-"

    approve_link.short_description = "Akcija"

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "<int:person_id>/approve/",
                self.admin_site.admin_view(self.approve_person),
                name="graves_person_approve",
            ),
        ]

        return custom_urls + urls

    def approve_person(self, request, person_id):
        person = Person.objects.get(id=person_id)

        person.status = Person.STATUS_APPROVED
        person.save(update_fields=["status"])

        return redirect("/admin/graves/person/")

    @admin.action(description="Odobri odabrane osobe")
    def approve_persons(self, request, queryset):
        queryset.update(
            status=Person.STATUS_APPROVED
        )

    @admin.action(description="Odbij odabrane osobe")
    def reject_persons(self, request, queryset):
        queryset.update(
            status=Person.STATUS_REJECTED
        )
    

@admin.register(Photo)
class PhotoAdmin(GISModelAdmin):
    list_display = ("id", "grave", "caption", "uploaded_at")


@admin.register(EditHistory)
class EditHistoryAdmin(admin.ModelAdmin):
    list_display = ("grave", "field_name", "edited_by", "edited_at")
    search_fields = ("field_name", "old_value", "new_value")


@admin.register(LocationSuggestion)
class LocationSuggestionAdmin(GISModelAdmin):
    list_display = ("grave", "suggested_by", "approval_badge", "created_at")
    list_filter = ("approved",)

    def approval_badge(self, obj):
        if obj.approved:
            label = "ODOBRENO"
            status_class = "wg-status-approved"
        else:
            label = "ČEKA PREGLED"
            status_class = "wg-status-pending"

        return format_html(
            '<span class="wg-status {}">{}</span>',
            status_class,
            label,
        )

    approval_badge.short_description = "Status"


@admin.register(EditSuggestion)
class EditSuggestionAdmin(admin.ModelAdmin):
    actions = ["approve_suggestions"]

    list_display = (
        "grave",
        "field_name",
        "suggested_by",
        "status_badge",
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

    fields = (
        "grave",
        "suggested_by",
        "field_name",
        "old_value",
        "new_value",
        "status",
        "admin_note",
    )
    
    readonly_fields = (
        "grave",
        "suggested_by",
        "field_name",
        "old_value",
        "created_at",
        "reviewed_at",
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

    def status_badge(self, obj):
        labels = {
            EditSuggestion.STATUS_APPROVED: "ODOBRENO",
            EditSuggestion.STATUS_PENDING: "PENDING",
            EditSuggestion.STATUS_REJECTED: "ODBIJENO",
        }

        status_class = {
            EditSuggestion.STATUS_APPROVED: "wg-status-approved",
            EditSuggestion.STATUS_PENDING: "wg-status-pending",
            EditSuggestion.STATUS_REJECTED: "wg-status-rejected",
        }.get(obj.status, "")

        return format_html(
            '<span class="wg-status {}">{}</span>',
            status_class,
            labels.get(obj.status, obj.status),
        )

    status_badge.short_description = "Status"
    
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
    "status_badge",
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

    def status_badge(self, obj):
        labels = {
            Comment.STATUS_APPROVED: "ODOBRENO",
            Comment.STATUS_PENDING: "PENDING",
            Comment.STATUS_REJECTED: "ODBIJENO",
        }

        status_class = {
            Comment.STATUS_APPROVED: "wg-status-approved",
            Comment.STATUS_PENDING: "wg-status-pending",
            Comment.STATUS_REJECTED: "wg-status-rejected",
        }.get(obj.status, "")

        return format_html(
            '<span class="wg-status {}">{}</span>',
            status_class,
            labels.get(obj.status, obj.status),
        )

    status_badge.short_description = "Status"
    
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

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = (
        "grave",
        "problem_type",
        "reported_by",
        "status_badge",
        "created_at",
    )

    list_filter = (
        "status",
        "problem_type",
        "created_at",
    )

    search_fields = (
        "grave__title",
        "description",
        "reported_by__username",
    )

    actions = [
        "mark_resolved",
        "mark_rejected",
    ]

    
    def status_badge(self, obj):
        labels = {
            ProblemReport.STATUS_OPEN: "OTVORENO",
            ProblemReport.STATUS_RESOLVED: "RIJEŠENO",
            ProblemReport.STATUS_REJECTED: "ODBIJENO",
        }

        status_class = {
            ProblemReport.STATUS_OPEN: "wg-status-pending",
            ProblemReport.STATUS_RESOLVED: "wg-status-approved",
            ProblemReport.STATUS_REJECTED: "wg-status-rejected",
        }.get(obj.status, "")

        return format_html(
            '<span class="wg-status {}">{}</span>',
            status_class,
            labels.get(obj.status, obj.status),
        )

    status_badge.short_description = "Status"

    @admin.action(description="Označi kao riješeno")
    def mark_resolved(self, request, queryset):
        queryset.update(status=ProblemReport.STATUS_RESOLVED)

    @admin.action(description="Označi kao odbijeno")
    def mark_rejected(self, request, queryset):
        queryset.update(status=ProblemReport.STATUS_REJECTED)
        
        
# =========================================================
# Wiki Greblje - Admin dashboard
# =========================================================

_original_admin_index = admin.site.index


def wiki_admin_index(request, extra_context=None):
    extra_context = extra_context or {}

    extra_context.update({
        "pending_graves_count": Grave.objects.filter(
            status=Grave.STATUS_PENDING
        ).count(),

        "pending_persons_count": Person.objects.filter(
            status=Person.STATUS_PENDING
        ).count(),

        "pending_comments_count": Comment.objects.filter(
            status=Comment.STATUS_PENDING
        ).count(),

        "pending_edit_suggestions_count": EditSuggestion.objects.filter(
            status=EditSuggestion.STATUS_PENDING
        ).count(),

        "pending_location_suggestions_count": LocationSuggestion.objects.filter(
            approved=False
        ).count(),

        "open_problem_reports_count": ProblemReport.objects.filter(
            status=ProblemReport.STATUS_OPEN
        ).count(),
    })

    return _original_admin_index(
        request,
        extra_context=extra_context,
    )


admin.site.index = wiki_admin_index