from django import forms
from django.contrib.gis.geos import Point

from .models import Grave, Photo, Person, EditSuggestion, PersonEditSuggestion, Comment, ProblemReport, LocationSuggestion

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
    
    ocr_photo = forms.ImageField(
        required=False,
        label="Fotografija natpisa",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
            }
        ),
    )
    
    photos = MultipleFileField(
        required=False,
        label="Fotografije groba"
    )

    primary_photo_index = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
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

    person_gender = forms.ChoiceField(
        required=False,
        label="Spol",
        choices=Person.GENDER_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "person-gender-select",
            }
        ),
    )

    person_photo = forms.ImageField(
        required=False,
        label="Fotografija osobe",
        widget=forms.ClearableFileInput(
            attrs={
                "accept": "image/*",
            }
        ),
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

            primary_photo_index = self.cleaned_data.get(
                "primary_photo_index"
            )

            if photos:
                if (
                    primary_photo_index is None
                    or primary_photo_index < 0
                    or primary_photo_index >= len(photos)
                ):
                    primary_photo_index = 0

            for index, photo in enumerate(photos):
                photo_status = (
                    Photo.STATUS_APPROVED
                    if user and user.is_staff
                    else Photo.STATUS_PENDING
                )

                Photo.objects.create(
                    grave=grave,
                    image=photo,
                    is_primary=(index == primary_photo_index),
                    uploaded_by=user if user else None,
                    status=photo_status,
                )

            first_name = (self.cleaned_data.get("first_name") or "").strip()
            last_name = (self.cleaned_data.get("last_name") or "").strip()

            unknown_values = {
                "nn",
                "n.n.",
                "n.n",
                "nepoznat",
                "nepoznata",
                "nepoznato",
                "nije poznato",
            }

            if first_name.lower() in unknown_values:
                first_name = ""

            if last_name.lower() in unknown_values:
                last_name = ""

            is_unknown = not first_name and not last_name

            if not grave.title and (first_name or last_name):
                grave.title = f"{first_name} {last_name}".strip()
                grave.save(update_fields=["title"])

            if first_name or last_name or is_unknown:
                Person.objects.create(
                    grave=grave,
                    first_name=first_name,
                    last_name=last_name,
                    is_unknown=is_unknown,
                    birth_year=self.cleaned_data.get("birth_year"),
                    death_year=self.cleaned_data.get("death_year"),
                    gender=self.cleaned_data.get("person_gender", ""),
                    photo=self.cleaned_data.get("person_photo"),
                    notes=self.cleaned_data.get("person_notes", ""),
                    status=Person.STATUS_PENDING,
                    created_by=user if user else None,
                )

        return grave

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "is_unknown",
            "first_name",
            "last_name",
            "birth_year",
            "death_year",
            "gender",
            "photo",
            "notes",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ime",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Prezime",
                }
            ),
            "birth_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Godina rođenja",
                }
            ),
            "death_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Godina smrti",
                }
            ),
            "gender": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "photo": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Dodatne potvrđene informacije o osobi",
                }
            ),
        }

        labels = {
            "first_name": "Ime",
            "last_name": "Prezime",
            "birth_year": "Godina rođenja",
            "death_year": "Godina smrti",
            "gender": "Spol",
            "photo": "Fotografija osobe",
            "notes": "Bilješke o osobi",
        }

    def clean(self):
        cleaned_data = super().clean()

        is_unknown = cleaned_data.get("is_unknown")
        first_name = (cleaned_data.get("first_name") or "").strip()
        last_name = (cleaned_data.get("last_name") or "").strip()

        unknown_values = {
            "nn",
            "n.n.",
            "n.n",
            "nepoznat",
            "nepoznata",
            "nepoznato",
            "nije poznato",
        }

        # Placeholder nije stvarno ime/prezime.
        if first_name.lower() in unknown_values:
            first_name = ""

        if last_name.lower() in unknown_values:
            last_name = ""

        # Ako je korisnik izričito označio osobu kao nepoznatu,
        # ne čuvamo tekst u poljima ime/prezime.
        if is_unknown:
            cleaned_data["first_name"] = ""
            cleaned_data["last_name"] = ""
            return cleaned_data

        # Ako nakon čišćenja nemamo ni ime ni prezime,
        # zapis tretiramo kao nepoznatu osobu.
        if not first_name and not last_name:
            cleaned_data["is_unknown"] = True
            cleaned_data["first_name"] = ""
            cleaned_data["last_name"] = ""
            return cleaned_data

        # Čuvamo svaki poznati dio identiteta.
        cleaned_data["first_name"] = first_name
        cleaned_data["last_name"] = last_name
        cleaned_data["is_unknown"] = False

        return cleaned_data


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

class PersonEditSuggestionForm(forms.ModelForm):

    class Meta:
        model = PersonEditSuggestion

        fields = [
            "field_name",
            "new_value",
        ]

        widgets = {
            "field_name": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "new_value": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                }
            ),
        }

        labels = {
            "field_name": "Polje koje predlažete izmijeniti",
            "new_value": "Nova vrijednost",
        }

class LocationSuggestionForm(forms.ModelForm):

    latitude = forms.FloatField(
        required=True,
        widget=forms.HiddenInput(),
    )

    longitude = forms.FloatField(
        required=True,
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = LocationSuggestion

        fields = [
            "reason",
        ]

        widgets = {
            "reason": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": "form-control",
                    "placeholder": (
                        "Ukratko navedite zašto predlažete "
                        "ispravku lokacije."
                    ),
                }
            ),
        }

        labels = {
            "reason": "Razlog ili napomena",
        }

    def save(self, commit=True):

        suggestion = super().save(commit=False)

        latitude = self.cleaned_data["latitude"]
        longitude = self.cleaned_data["longitude"]

        suggestion.suggested_location = Point(
            float(longitude),
            float(latitude),
            srid=4326,
        )

        if commit:
            suggestion.save()

        return suggestion
    
    
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