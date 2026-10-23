from django import forms
from django.conf import settings
from django.contrib.gis.geos import Point

from .models import (
    Cemetery,
    Comment,
    EditSuggestion,
    Grave,
    LocationSuggestion,
    MonumentCondition,
    MonumentMacroType,
    MonumentPosition,
    MonumentTradition,
    MonumentType,
    Person,
    PersonEditSuggestion,
    Photo,
    ProblemReport,
)

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


class SearchFilterForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Pojam za pretragu",
    )
    cemetery = forms.ModelChoiceField(
        queryset=Cemetery.objects.none(),
        required=False,
        empty_label="Sva groblja",
        label="Groblje",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    location = forms.CharField(
        required=False,
        max_length=100,
        label="Grad ili selo",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Npr. Visoko ili Rostovo",
            }
        ),
    )
    birth_year_from = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=9999,
        label="Rođeni od",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Od"}
        ),
    )
    birth_year_to = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=9999,
        label="Rođeni do",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Do"}
        ),
    )
    death_year_from = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=9999,
        label="Umrli od",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Od"}
        ),
    )
    death_year_to = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=9999,
        label="Umrli do",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Do"}
        ),
    )
    macro_type = forms.ModelChoiceField(
        queryset=MonumentMacroType.objects.none(),
        required=False,
        empty_label="Svi makro-tipovi",
        label="Makro-tip",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    tradition = forms.ModelChoiceField(
        queryset=MonumentTradition.objects.none(),
        required=False,
        empty_label="Sve tradicije",
        label="Tradicija",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    monument_type = forms.ModelChoiceField(
        queryset=MonumentType.objects.none(),
        required=False,
        empty_label="Svi tipovi spomenika",
        label="Tip spomenika",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    condition_classification = forms.ModelChoiceField(
        queryset=MonumentCondition.objects.none(),
        required=False,
        empty_label="Sva stanja",
        label="Stanje spomenika",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    monument_position = forms.ModelChoiceField(
        queryset=MonumentPosition.objects.none(),
        required=False,
        empty_label="Svi položaji",
        label="Položaj spomenika",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        public_graves = {
            "graves__status": Grave.STATUS_APPROVED,
            "graves__cemetery__status": Cemetery.STATUS_APPROVED,
        }

        self.fields["cemetery"].queryset = Cemetery.objects.filter(
            status=Cemetery.STATUS_APPROVED,
        ).order_by("name")

        classification_models = {
            "macro_type": MonumentMacroType,
            "tradition": MonumentTradition,
            "monument_type": MonumentType,
            "condition_classification": MonumentCondition,
            "monument_position": MonumentPosition,
        }

        for field_name, model in classification_models.items():
            self.fields[field_name].queryset = (
                model.objects
                .filter(is_active=True, **public_graves)
                .distinct()
                .order_by("sort_order", "code")
            )

    def clean(self):
        cleaned_data = super().clean()

        year_ranges = (
            ("birth_year_from", "birth_year_to"),
            ("death_year_from", "death_year_to"),
        )

        for start_name, end_name in year_ranges:
            start_year = cleaned_data.get(start_name)
            end_year = cleaned_data.get(end_name)

            if (
                start_year is not None
                and end_year is not None
                and start_year > end_year
            ):
                self.add_error(
                    end_name,
                    "Završna godina mora biti jednaka ili veća od početne.",
                )

        return cleaned_data

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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user
        # Samo odobrena groblja mogu se birati
        # prilikom javnog predlaganja groba.
        self.fields["cemetery"].queryset = Cemetery.objects.filter(
            status=Cemetery.STATUS_APPROVED
        ).order_by("name")

        is_editor = bool(
            user
            and user.is_authenticated
            and user.groups.filter(name="Urednici").exists()
        )

        is_expert = bool(
            user
            and user.is_authenticated
            and user.groups.filter(name="Stručnjaci").exists()
        )

        basic_classification_fields = (
            "macro_type",
            "tradition",
            "monument_type",
            "condition_classification",
            "monument_position",
            "condition_notes",
        )

        expert_classification_fields = (
            "motifs",
            "deterioration_patterns",
        )

        if not is_editor:
            for field_name in basic_classification_fields:
                self.fields.pop(field_name, None)

        if not (is_editor and is_expert):
            for field_name in expert_classification_fields:
                self.fields.pop(field_name, None)

    class Meta:
        model = Grave
        fields = [
            "cemetery",
            "title",
            "inscription",
            "condition",
            "notes",
            "macro_type",
            "tradition",
            "monument_type",
            "motifs",
            "condition_classification",
            "deterioration_patterns",
            "monument_position",
            "condition_notes",
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
            has_person_data = any([
                first_name,
                last_name,
                self.cleaned_data.get("birth_year") is not None,
                self.cleaned_data.get("death_year") is not None,
                self.cleaned_data.get("person_gender"),
                self.cleaned_data.get("person_photo"),
                (self.cleaned_data.get("person_notes") or "").strip(),
            ])
            if not grave.title and (first_name or last_name):
                grave.title = f"{first_name} {last_name}".strip()
                grave.save(update_fields=["title"])

            if has_person_data:
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

class CemeteryProposalForm(forms.ModelForm):
    latitude = forms.FloatField(
        required=False,
        label="Geografska širina",
        widget=forms.HiddenInput(),
    )

    longitude = forms.FloatField(
        required=False,
        label="Geografska dužina",
        widget=forms.HiddenInput(),
    )

    photos = MultipleFileField(
        required=False,
        label="Fotografije groblja",
        widget=MultipleFileInput(attrs={
            "accept": "image/*",
        }),
    )

    class Meta:
        model = Cemetery
        fields = [
            "name",
            "cemetery_type",
            "city",
            "village",
            "description",
        ]
        labels = {
            "name": "Naziv groblja",
            "cemetery_type": "Vrsta groblja",
            "city": "Grad",
            "village": "Naselje / selo",
            "description": "Opis groblja",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["latitude"].widget.attrs["data-maptiler-key"] = (
            settings.MAPTILER_API_KEY
        )
    def clean(self):
        cleaned_data = super().clean()

        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        if (latitude is None) != (longitude is None):
            raise forms.ValidationError(
                "Potrebno je unijeti obje koordinate ili nijednu."
            )

        return cleaned_data
