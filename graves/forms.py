from django import forms
from django.contrib.gis.geos import Point

from .models import Grave, Photo, Person, EditSuggestion, Comment, ProblemReport

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []

        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(d, initial) for d in data]

        return [super().clean(data, initial)]

class PublicGraveForm(forms.ModelForm):
    latitude = forms.FloatField(required=False,widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False,widget=forms.HiddenInput())
    photos = MultipleFileField(
        required=False,
        label="Fotografije"
    )

    first_name = forms.CharField(
        max_length=100,
        required=False,
        label="Ime osobe"
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
        label="Prezime osobe"
    )

    birth_year = forms.IntegerField(
        required=False,
        label="Godina rođenja"
    )

    death_year = forms.IntegerField(
        required=False,
        label="Godina smrti"
    )

    person_notes = forms.CharField(
        required=False,
        label="Napomena o osobi",
        widget=forms.Textarea(attrs={"rows": 3})
    )

    class Meta:
        model = Grave
        fields = [
            "cemetery",
            "title",
            "inscription",
            "condition",
            "notes",
        ]

    def save(self, user=None, commit=True):
        grave = super().save(commit=False)
        grave.status = Grave.STATUS_PENDING


        if user:
            grave.created_by = user

        lat = self.cleaned_data.get("latitude")
        lon = self.cleaned_data.get("longitude")

        if lat and lon:
            grave.location = Point(
                float(lon),
                float(lat),
                srid=4326
            )
            
        if commit:
            grave.save()

            photos = self.cleaned_data.get("photos", [])

            for photo in photos:
                Photo.objects.create(
                    grave=grave,
                    image=photo,
                    uploaded_by=user if user else None,
                )

            first_name = self.cleaned_data.get("first_name")
            last_name = self.cleaned_data.get("last_name")

            if not grave.title and (first_name or last_name):
                grave.title = f"{first_name or ''} {last_name or ''}".strip()
                grave.save(update_fields=["title"])
            if first_name or last_name:
                Person.objects.create(
                    grave=grave,
                    first_name=first_name or "",
                    last_name=last_name or "",
                    birth_year=self.cleaned_data.get("birth_year"),
                    death_year=self.cleaned_data.get("death_year"),
                    notes=self.cleaned_data.get("person_notes", ""),
                )

        return grave

class EditSuggestionForm(forms.ModelForm):
    class Meta:
        model = EditSuggestion
        fields = [
            "field_name",
            "new_value",
        ]

        widgets = {
            "new_value": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
            }),
            "field_name": forms.Select(attrs={
                "class": "form-control",
            }),
        }

        labels = {
            "field_name": "Polje koje predlažete izmijeniti",
            "new_value": "Nova vrijednost",
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
            "photo",
        ]

        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Unesite dodatne informacije, predanje, pretpostavku ili komentar..."
            }),
            "photo": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
        }

        labels = {
            "text": "Komentar",
            "photo": "Fotografija"
        }
        
class ProblemReportForm(forms.ModelForm):
    class Meta:
        model = ProblemReport
        fields = [
            "problem_type",
            "description",
        ]

        widgets = {
            "problem_type": forms.Select(attrs={
                "class": "form-control",
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "form-control",
                "placeholder": "Opišite problem..."
            }),
        }

        labels = {
            "problem_type": "Vrsta problema",
            "description": "Opis problema",
        }