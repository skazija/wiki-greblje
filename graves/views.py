import os
from unicodedata import combining, normalize

import easyocr
import pytesseract
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
from django.db.models import Prefetch
from .models import EditSuggestion    
from django.shortcuts import render, get_object_or_404
from django.db.models import Case, IntegerField, Q, TextField, Value, When
from django.db.models.functions import Concat, Lower, Replace
from django.core.paginator import Paginator
from .models import Cemetery, Grave, Person, Photo, EditSuggestion, PersonEditSuggestion, Comment, ProblemReport, CemeteryPhoto, LocationSuggestion

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings

from .forms import (
    CemeteryProposalForm,
    CommentForm,
    EditSuggestionForm,
    LocationSuggestionForm,
    PersonEditSuggestionForm,
    PersonForm,
    ProblemReportForm,
    PublicGraveForm,
    SearchFilterForm,
)
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.db.models import Count
from django.http import Http404

from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from django.contrib.admin.views.decorators import staff_member_required
from .services.ocr.engine import recognize_inscription

from PIL import Image
from .models import Photo


def cemetery_list(request):
    cemeteries = (
        Cemetery.objects
        .filter(status=Cemetery.STATUS_APPROVED)
        .prefetch_related("photos")
        .order_by("name")
    )

    return render(request, "graves/cemetery_list.html", {
        "cemeteries": cemeteries,
    })


def cemetery_detail(request, pk):
    cemetery = get_object_or_404(Cemetery,pk=pk,status=Cemetery.STATUS_APPROVED,)

    graves = cemetery.graves.filter(
        status=Grave.STATUS_APPROVED
    ).prefetch_related(
        Prefetch(
            "photos",
            queryset=Photo.objects.filter(
                status=Photo.STATUS_APPROVED
            ).order_by(
                "-is_primary",
                "id",
            ),
            to_attr="approved_photos",
        ),
        Prefetch(
            "persons",
            queryset=Person.objects.filter(
                status=Person.STATUS_APPROVED
            ),
            to_attr="approved_persons",
        )
    )

    cemetery_photos = cemetery.photos.filter(
        status=CemeteryPhoto.STATUS_APPROVED
    ).order_by(
        "-is_primary",
        "id"
    )

    primary_photo = cemetery_photos.filter(
        is_primary=True
    ).first()

    if not primary_photo:
        primary_photo = cemetery_photos.first()

    return render(request, "graves/cemetery_detail.html", {
        "cemetery": cemetery,
        "graves": graves,
        "cemetery_photos": cemetery_photos,
        "primary_photo": primary_photo,
        "maptiler_api_key": settings.MAPTILER_API_KEY,
    })


def grave_detail(request, pk):

    grave = get_object_or_404(Grave, pk=pk)

    if grave.cemetery.status != Cemetery.STATUS_APPROVED:
        if (
            not request.user.is_authenticated
            or (
                request.user != grave.cemetery.created_by
                and not request.user.has_perm("graves.change_cemetery")
            )
        ):
            raise Http404()
    if grave.status != Grave.STATUS_APPROVED:

        if request.user != grave.created_by and not request.user.is_staff:
            raise Http404()

        return render(request, "graves/grave_pending.html", {
            "grave": grave
        })

    edit_history = grave.edit_history.select_related(
        "edited_by"
    ).order_by("-edited_at")[:10]

    related_persons = Person.objects.none()

    last_names = grave.persons.filter(
        status=Person.STATUS_APPROVED,
        is_unknown=False,
    ).exclude(
        last_name=""
    ).exclude(
        Q(last_name__iexact="nepoznat") |
        Q(last_name__iexact="nepoznata") |
        Q(last_name__iexact="nepoznato") |
        Q(last_name__iexact="nn") |
        Q(last_name__iexact="n.n.") |
        Q(last_name__iexact="nije poznato")
    ).values_list(
        "last_name",
        flat=True
    ).distinct()

    if last_names:
        related_persons = Person.objects.filter(
            last_name__in=last_names,
            grave__status=Grave.STATUS_APPROVED,
            status=Person.STATUS_APPROVED,
            is_unknown=False,
        ).exclude(
            grave=grave
        ).select_related(
            "grave",
            "grave__cemetery"
        ).order_by(
            "death_year",
            "birth_year"
        )[:20]
    comments = grave.comments.filter(
        status=Comment.STATUS_APPROVED
    ).select_related("author").order_by("-created_at")

    comment_form = CommentForm()

    nearby_graves = []

    if grave.location:
        nearby_graves = (
            Grave.objects
            .filter(
                cemetery=grave.cemetery,
                status=Grave.STATUS_APPROVED,
                location__isnull=False,
                location__distance_lte=(grave.location, D(m=50)),
            )                
            .exclude(id=grave.id)
            .annotate(distance=Distance("location", grave.location))
            .order_by("distance")[:10]
        )
    grave_photos = grave.photos.filter(
        status=Photo.STATUS_APPROVED
    ).order_by(
        "-is_primary",
        "id"
    )
    
    approved_persons = grave.persons.filter(
        status=Person.STATUS_APPROVED
    )
    
    pending_persons_count = grave.persons.filter(
        status=Person.STATUS_PENDING
    ).count()
    
    return render(request, "graves/grave_detail.html", {
        "grave": grave,
        "approved_persons": approved_persons,
        "pending_persons_count": pending_persons_count,
        "grave_photos": grave_photos,
        "edit_history": edit_history,
        "related_persons": related_persons,
        "comments": comments,
        "comment_form": comment_form,
        "nearby_graves": nearby_graves,
        "maptiler_api_key": settings.MAPTILER_API_KEY,
    })


SEARCH_CHARACTER_REPLACEMENTS = (
    ("č", "c"),
    ("ć", "c"),
    ("š", "s"),
    ("ž", "z"),
    ("đ", "dj"),
    ("\u0301", ""),
    ("\u030c", ""),
)


def _normalize_search_text(value):
    normalized_value = normalize(
        "NFKD",
        value.casefold().replace("đ", "dj"),
    )
    return "".join(
        character
        for character in normalized_value
        if not combining(character)
    )


def _normalized_search_expression(field_name):
    expression = Lower(field_name)

    for source, replacement in SEARCH_CHARACTER_REPLACEMENTS:
        expression = Replace(
            expression,
            Value(source),
            Value(replacement),
            output_field=TextField(),
        )

    return expression


def _person_search_token_query(token):
    token_query = (
        Q(search_first_name__contains=token) |
        Q(search_last_name__contains=token) |
        Q(search_birth_date__contains=token) |
        Q(search_death_date__contains=token)
    )

    if token.isascii() and token.isdigit() and len(token) <= 4:
        year = int(token)
        token_query |= (
            Q(birth_year=year) |
            Q(death_year=year)
        )

    # Support a common Bosnian name form such as "Rasima" when the
    # stored nominative form is "Rasim", without enabling broad fuzzy
    # matching for unrelated names.
    if len(token) >= 5 and token.casefold().endswith("a"):
        nominative_candidate = token[:-1]
        token_query |= (
            Q(search_first_name=nominative_candidate) |
            Q(search_last_name=nominative_candidate)
        )

    return token_query


def _person_name_query_variants(tokens):
    if not tokens:
        return ()

    variants = {" ".join(tokens)}
    stripped_tokens = list(tokens)

    for index, token in enumerate(tokens):
        if len(token) >= 5 and token.endswith("a"):
            variant_tokens = list(tokens)
            variant_tokens[index] = token[:-1]
            stripped_tokens[index] = token[:-1]
            variants.add(" ".join(variant_tokens))

    variants.add(" ".join(stripped_tokens))
    return tuple(variants)


def _text_search_querysets(query):
    if query:
        query_tokens = [
            _normalize_search_text(token)
            for token in query.split()
        ]
        normalized_query = " ".join(query_tokens)

        cemeteries = (
            Cemetery.objects
            .filter(status=Cemetery.STATUS_APPROVED)
            .annotate(
                search_name=_normalized_search_expression("name"),
                search_city=_normalized_search_expression("city"),
                search_village=_normalized_search_expression("village"),
            )
        )

        for token in query_tokens:
            cemeteries = cemeteries.filter(
                Q(search_name__contains=token) |
                Q(search_city__contains=token) |
                Q(search_village__contains=token)
            )

        cemeteries = cemeteries.annotate(
            search_rank=Case(
                When(search_name=normalized_query, then=Value(0)),
                When(
                    search_name__startswith=normalized_query,
                    then=Value(1),
                ),
                When(
                    search_name__contains=normalized_query,
                    then=Value(2),
                ),
                When(
                    Q(search_city=normalized_query) |
                    Q(search_village=normalized_query),
                    then=Value(3),
                ),
                When(
                    Q(search_city__startswith=normalized_query) |
                    Q(search_village__startswith=normalized_query),
                    then=Value(4),
                ),
                When(
                    Q(search_city__contains=normalized_query) |
                    Q(search_village__contains=normalized_query),
                    then=Value(5),
                ),
                default=Value(6),
                output_field=IntegerField(),
            )
        ).order_by("search_rank", "name", "id")

        graves = (
            Grave.objects
            .filter(
                status=Grave.STATUS_APPROVED,
                cemetery__status=Cemetery.STATUS_APPROVED,
            )
            .select_related("cemetery")
            .annotate(
                search_title=_normalized_search_expression("title"),
                search_inscription=_normalized_search_expression(
                    "inscription"
                ),
                search_cemetery_name=_normalized_search_expression(
                    "cemetery__name"
                ),
            )
        )

        for token in query_tokens:
            graves = graves.filter(
                Q(search_title__contains=token) |
                Q(search_inscription__contains=token) |
                Q(search_cemetery_name__contains=token)
            )

        grave_content_conditions = [
            Q(search_title__contains=token) |
            Q(search_inscription__contains=token)
            for token in query_tokens
        ]
        grave_content_match = grave_content_conditions[0]

        for condition in grave_content_conditions[1:]:
            grave_content_match |= condition

        # The cemetery name can provide context for a grave query, but a
        # cemetery-only query should return the cemetery as its own result
        # instead of listing every grave in that cemetery.
        graves = graves.filter(grave_content_match)

        graves = graves.annotate(
            search_rank=Case(
                When(search_title=normalized_query, then=Value(0)),
                When(
                    search_title__startswith=normalized_query,
                    then=Value(1),
                ),
                When(
                    search_title__contains=normalized_query,
                    then=Value(2),
                ),
                When(
                    search_inscription__contains=normalized_query,
                    then=Value(3),
                ),
                When(
                    search_cemetery_name=normalized_query,
                    then=Value(4),
                ),
                When(
                    search_cemetery_name__startswith=normalized_query,
                    then=Value(5),
                ),
                default=Value(6),
                output_field=IntegerField(),
            )
        ).order_by("search_rank", "id")

        persons = (
            Person.objects
            .filter(
                grave__status=Grave.STATUS_APPROVED,
                grave__cemetery__status=Cemetery.STATUS_APPROVED,
                status=Person.STATUS_APPROVED,
            )
            .select_related(
                "grave",
                "grave__cemetery",
            )
            .annotate(
                search_first_name=_normalized_search_expression(
                    "first_name"
                ),
                search_last_name=_normalized_search_expression(
                    "last_name"
                ),
                search_birth_date=_normalized_search_expression(
                    "birth_date_text"
                ),
                search_death_date=_normalized_search_expression(
                    "death_date_text"
                ),
            )
            .annotate(
                search_full_name=Concat(
                    "search_first_name",
                    Value(" "),
                    "search_last_name",
                    output_field=TextField(),
                ),
                search_reverse_name=Concat(
                    "search_last_name",
                    Value(" "),
                    "search_first_name",
                    output_field=TextField(),
                ),
            )
        )

        for token in query_tokens:
            persons = persons.filter(
                _person_search_token_query(token)
            )

        name_tokens = [
            token
            for token in query_tokens
            if not (
                token.isascii() and
                token.isdigit() and
                len(token) <= 4
            )
        ]
        name_query_variants = _person_name_query_variants(name_tokens)

        person_rank_conditions = []

        if name_query_variants:
            exact_full_name_conditions = []
            exact_name_field_conditions = []
            starts_with_name_conditions = []
            contains_name_conditions = []

            for name_query in name_query_variants:
                exact_full_name_conditions.append(
                    Q(search_full_name=name_query) |
                    Q(search_reverse_name=name_query)
                )
                exact_name_field_conditions.append(
                    Q(search_first_name=name_query) |
                    Q(search_last_name=name_query)
                )
                starts_with_name_conditions.append(
                    Q(search_full_name__startswith=name_query) |
                    Q(search_reverse_name__startswith=name_query) |
                    Q(search_first_name__startswith=name_query) |
                    Q(search_last_name__startswith=name_query)
                )
                contains_name_conditions.append(
                    Q(search_full_name__contains=name_query) |
                    Q(search_reverse_name__contains=name_query) |
                    Q(search_first_name__contains=name_query) |
                    Q(search_last_name__contains=name_query)
                )

            exact_full_name = exact_full_name_conditions[0]
            exact_name_field = exact_name_field_conditions[0]
            starts_with_name = starts_with_name_conditions[0]
            contains_name = contains_name_conditions[0]

            for condition in exact_full_name_conditions[1:]:
                exact_full_name |= condition
            for condition in exact_name_field_conditions[1:]:
                exact_name_field |= condition
            for condition in starts_with_name_conditions[1:]:
                starts_with_name |= condition
            for condition in contains_name_conditions[1:]:
                contains_name |= condition

            person_rank_conditions = [
                When(exact_full_name, then=Value(0)),
                When(exact_name_field, then=Value(1)),
                When(starts_with_name, then=Value(2)),
                When(contains_name, then=Value(3)),
            ]

        if person_rank_conditions:
            persons = persons.annotate(
                search_rank=Case(
                    *person_rank_conditions,
                    default=Value(4),
                    output_field=IntegerField(),
                )
            )
        else:
            persons = persons.annotate(
                search_rank=Value(
                    4,
                    output_field=IntegerField(),
                )
            )

        persons = persons.order_by(
            "search_rank",
            "last_name",
            "first_name",
            "id",
        )

        return cemeteries, graves, persons


SEARCH_FILTER_NAMES = (
    "cemetery",
    "location",
    "birth_year_from",
    "birth_year_to",
    "death_year_from",
    "death_year_to",
    "macro_type",
    "tradition",
    "monument_type",
    "condition_classification",
    "monument_position",
)


def search(request):
    search_form = SearchFilterForm(request.GET or None)
    form_submitted = bool(request.GET)
    form_valid = search_form.is_valid() if form_submitted else False
    cleaned_data = search_form.cleaned_data if form_valid else {}

    query = (
        (cleaned_data.get("q") or "").strip()
        if form_valid
        else request.GET.get("q", "").strip()
    )
    filters_active = bool(
        form_valid
        and any(
            cleaned_data.get(field_name) not in (None, "")
            for field_name in SEARCH_FILTER_NAMES
        )
    )
    active_filter_count = (
        sum(
            cleaned_data.get(field_name) not in (None, "")
            for field_name in SEARCH_FILTER_NAMES
        )
        if form_valid
        else 0
    )
    has_search = bool(form_valid and (query or filters_active))

    cemeteries_page = None
    graves_page = None
    persons_page = None
    map_cemeteries = []
    map_graves = []

    if has_search:
        if query:
            cemeteries, graves, persons = _text_search_querysets(query)
        else:
            cemeteries = Cemetery.objects.filter(
                status=Cemetery.STATUS_APPROVED,
            )
            graves = (
                Grave.objects
                .filter(
                    status=Grave.STATUS_APPROVED,
                    cemetery__status=Cemetery.STATUS_APPROVED,
                )
                .select_related("cemetery")
            )
            persons = (
                Person.objects
                .filter(
                    status=Person.STATUS_APPROVED,
                    grave__status=Grave.STATUS_APPROVED,
                    grave__cemetery__status=Cemetery.STATUS_APPROVED,
                )
                .select_related("grave", "grave__cemetery")
            )

        selected_cemetery = cleaned_data.get("cemetery")

        if selected_cemetery:
            cemeteries = cemeteries.filter(pk=selected_cemetery.pk)
            graves = graves.filter(cemetery=selected_cemetery)
            persons = persons.filter(grave__cemetery=selected_cemetery)

        location = _normalize_search_text(
            cleaned_data.get("location") or ""
        )

        if location:
            cemeteries = cemeteries.annotate(
                filter_city=_normalized_search_expression("city"),
                filter_village=_normalized_search_expression("village"),
            ).filter(
                Q(filter_city__contains=location) |
                Q(filter_village__contains=location)
            )
            graves = graves.annotate(
                filter_city=_normalized_search_expression(
                    "cemetery__city"
                ),
                filter_village=_normalized_search_expression(
                    "cemetery__village"
                ),
            ).filter(
                Q(filter_city__contains=location) |
                Q(filter_village__contains=location)
            )
            persons = persons.annotate(
                filter_city=_normalized_search_expression(
                    "grave__cemetery__city"
                ),
                filter_village=_normalized_search_expression(
                    "grave__cemetery__village"
                ),
            ).filter(
                Q(filter_city__contains=location) |
                Q(filter_village__contains=location)
            )

        grave_filter_kwargs = {}
        person_filter_kwargs = {}
        cemetery_related_filter_kwargs = {}

        classification_fields = (
            "macro_type",
            "tradition",
            "monument_type",
            "condition_classification",
            "monument_position",
        )

        for field_name in classification_fields:
            selected_value = cleaned_data.get(field_name)

            if selected_value:
                grave_filter_kwargs[field_name] = selected_value
                person_filter_kwargs[
                    f"grave__{field_name}"
                ] = selected_value
                cemetery_related_filter_kwargs[
                    f"graves__{field_name}"
                ] = selected_value

        year_lookups = (
            ("birth_year_from", "birth_year__gte"),
            ("birth_year_to", "birth_year__lte"),
            ("death_year_from", "death_year__gte"),
            ("death_year_to", "death_year__lte"),
        )

        for form_field, model_lookup in year_lookups:
            year = cleaned_data.get(form_field)

            if year is not None:
                person_filter_kwargs[model_lookup] = year
                grave_filter_kwargs[f"persons__{model_lookup}"] = year
                cemetery_related_filter_kwargs[
                    f"graves__persons__{model_lookup}"
                ] = year

        if grave_filter_kwargs:
            if any(
                lookup.startswith("persons__")
                for lookup in grave_filter_kwargs
            ):
                grave_filter_kwargs[
                    "persons__status"
                ] = Person.STATUS_APPROVED

            graves = graves.filter(**grave_filter_kwargs).distinct()

        if person_filter_kwargs:
            persons = persons.filter(**person_filter_kwargs).distinct()

        if cemetery_related_filter_kwargs:
            cemetery_related_filter_kwargs[
                "graves__status"
            ] = Grave.STATUS_APPROVED

            if any(
                lookup.startswith("graves__persons__")
                for lookup in cemetery_related_filter_kwargs
            ):
                cemetery_related_filter_kwargs[
                    "graves__persons__status"
                ] = Person.STATUS_APPROVED

            cemeteries = cemeteries.filter(
                **cemetery_related_filter_kwargs
            ).distinct()

        if not query:
            cemeteries = cemeteries.order_by("name", "id")
            graves = graves.order_by("id")
            persons = persons.order_by(
                "last_name",
                "first_name",
                "id",
            )

        cemeteries_paginator = Paginator(cemeteries, 10)
        graves_paginator = Paginator(graves, 10)
        persons_paginator = Paginator(persons, 10)

        cemeteries_page = cemeteries_paginator.get_page(
            request.GET.get("cemeteries_page")
        )
        graves_page = graves_paginator.get_page(
            request.GET.get("graves_page")
        )
        persons_page = persons_paginator.get_page(
            request.GET.get("persons_page")
        )

        grave_ids = set()

        for cemetery in cemeteries_page:
            if cemetery.location:
                map_cemeteries.append(cemetery)

        for grave in graves_page:
            if grave.location and grave.id not in grave_ids:
                grave_ids.add(grave.id)
                map_graves.append(grave)

        for person in persons_page:
            grave = person.grave

            if grave.location and grave.id not in grave_ids:
                grave_ids.add(grave.id)
                map_graves.append(grave)

    pagination_parameters = request.GET.copy()

    for page_parameter in (
        "cemeteries_page",
        "persons_page",
        "graves_page",
    ):
        pagination_parameters.pop(page_parameter, None)

    for parameter_name in list(pagination_parameters):
        if not pagination_parameters.get(parameter_name):
            pagination_parameters.pop(parameter_name)

    return render(
        request,
        "graves/search.html",
        {
            "query": query,
            "search_form": search_form,
            "has_search": has_search,
            "filters_active": filters_active,
            "active_filter_count": active_filter_count,
            "pagination_query": pagination_parameters.urlencode(),
            "cemeteries": cemeteries_page,
            "graves": graves_page,
            "persons": persons_page,
            "map_cemeteries": map_cemeteries,
            "map_graves": map_graves,
            "maptiler_api_key": settings.MAPTILER_API_KEY,
        },
    )

def home(request):
    cemetery_count = Cemetery.objects.filter(status=Cemetery.STATUS_APPROVED).count()
    grave_count = Grave.objects.filter(status=Grave.STATUS_APPROVED,cemetery__status=Cemetery.STATUS_APPROVED,).count()
    person_count = Person.objects.filter( status=Person.STATUS_APPROVED, grave__cemetery__status=Cemetery.STATUS_APPROVED, grave__status=Grave.STATUS_APPROVED,).count()
    photo_count = Photo.objects.filter(status=Photo.STATUS_APPROVED, grave__cemetery__status=Cemetery.STATUS_APPROVED, grave__status=Grave.STATUS_APPROVED,).count()
    user_count = User.objects.count()

    latest_graves = (
        Grave.objects
        .filter(
            status=Grave.STATUS_APPROVED, cemetery__status=Cemetery.STATUS_APPROVED,
        )
        .prefetch_related(
            Prefetch(
                "photos",
                queryset=Photo.objects.filter(
                    status=Photo.STATUS_APPROVED
                ).order_by(
                    "-is_primary",
                    "id",
                ),
                to_attr="approved_photos",
            ),
            Prefetch(
                "persons",
                queryset=Person.objects.filter(
                    status=Person.STATUS_APPROVED
                ),
                to_attr="approved_persons",
            ),
        )
        .order_by("-created_at")[:6]
    )

    latest_photos = Photo.objects.filter(
        status=Photo.STATUS_APPROVED,
        grave__status=Grave.STATUS_APPROVED,
        grave__cemetery__status=Cemetery.STATUS_APPROVED,
    ).select_related(
        "grave",
        "grave__cemetery"
    ).order_by("-uploaded_at")[:8]
    
    return render(request, "graves/home.html", {
        "cemetery_count": cemetery_count,
        "grave_count": grave_count,
        "person_count": person_count,
        "photo_count": photo_count,
        "latest_graves": latest_graves,
        "latest_photos": latest_photos,
        "user_count": user_count,
    })

@login_required
def propose_cemetery(request):
    if request.method == "POST":
        form = CemeteryProposalForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            cemetery = form.save(commit=False)

            cemetery.created_by = request.user
            cemetery.status = Cemetery.STATUS_PENDING

            latitude = form.cleaned_data.get("latitude")
            longitude = form.cleaned_data.get("longitude")

            if latitude is not None and longitude is not None:
                cemetery.latitude = latitude
                cemetery.longitude = longitude
                cemetery.location = Point(
                    longitude,
                    latitude,
                    srid=4326,
                )

            cemetery.save()

            for uploaded_photo in form.cleaned_data["photos"]:
                CemeteryPhoto.objects.create(
                    cemetery=cemetery,
                    image=uploaded_photo,
                    uploaded_by=request.user,
                    status=CemeteryPhoto.STATUS_PENDING,
                )

            return redirect(
                "graves:cemetery_proposal_success"
            )

    else:
        form = CemeteryProposalForm()

    return render(
        request,
        "graves/propose_cemetery.html",
        {
            "form": form,
            "maptiler_api_key": settings.MAPTILER_API_KEY,
        },
    )

@login_required
def cemetery_proposal_success(request):
    return render(
        request,
        "graves/cemetery_proposal_success.html",
    )

@login_required
def add_grave(request):
    if request.method == "POST":
        form = PublicGraveForm(
            request.POST,
            request.FILES,
            user=request.user,
        )

        if form.is_valid():
            grave = form.save(user=request.user)

            return redirect("graves:grave_detail",pk=grave.pk,)
    else:
        form = PublicGraveForm(
            user=request.user,
        )

    return render(request, "graves/add_grave.html", {
        "form": form,
        "maptiler_api_key": settings.MAPTILER_API_KEY,
    })

@login_required
def add_person(request, pk):
    grave = get_object_or_404(
        Grave,
        pk=pk,
    )

    if grave.status == Grave.STATUS_APPROVED:
        pass

    elif (
        grave.status == Grave.STATUS_PENDING
        and (
            request.user == grave.created_by
            or request.user.is_staff
        )
    ):
        pass

    else:
        raise Http404()

    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES)

        if form.is_valid():
            person = form.save(commit=False)
            person.grave = grave
            person.created_by = request.user

            if request.user.is_staff:
                person.status = Person.STATUS_APPROVED
            else:
                person.status = Person.STATUS_PENDING

            person.save()

            return redirect(
                "graves:grave_detail",
                pk=grave.pk,
            )
    else:
        form = PersonForm()

    return render(
        request,
        "graves/add_person.html",
        {
            "form": form,
            "grave": grave,
        },
    )

@login_required
def choose_grave_for_person(request):

    cemeteries = Cemetery.objects.filter(status=Cemetery.STATUS_APPROVED).order_by("name")

    selected_cemetery_id = request.GET.get("cemetery")
    selected_grave_id = request.GET.get("grave")

    graves = Grave.objects.none()

    if selected_cemetery_id:
        graves = Grave.objects.filter(
            cemetery_id=selected_cemetery_id,
            cemetery__status=Cemetery.STATUS_APPROVED,
            status=Grave.STATUS_APPROVED,
        ).order_by("title", "id")

    if selected_grave_id:
        grave = get_object_or_404(
            Grave,
            pk=selected_grave_id,
            status=Grave.STATUS_APPROVED,
            cemetery__status=Cemetery.STATUS_APPROVED,
        )

        return redirect(
            "graves:add_person",
            pk=grave.pk,
        )

    return render(
        request,
        "graves/choose_grave_for_person.html",
        {
            "cemeteries": cemeteries,
            "graves": graves,
            "selected_cemetery_id": selected_cemetery_id,
        },
    )


@login_required
def my_graves(request):
    graves = Grave.objects.filter(
        created_by=request.user
    ).select_related("cemetery").annotate(
        photo_count=Count("photos")
    ).order_by("-created_at")

    return render(request, "graves/my_graves.html", {
        "graves": graves,
    })

def cemetery_location_api(request, pk):
    cemetery = get_object_or_404(Cemetery,pk=pk,status=Cemetery.STATUS_APPROVED,)

    if not cemetery.location:
        return JsonResponse({})

    return JsonResponse({
        "lat": cemetery.location.y,
        "lng": cemetery.location.x,
    })

@login_required
def profile(request):

    user_graves = Grave.objects.filter(
        created_by=request.user
    )

    user_persons = Person.objects.filter(
        created_by=request.user
    )

    user_grave_photos = Photo.objects.filter(
        uploaded_by=request.user
    )

    user_cemetery_photos = CemeteryPhoto.objects.filter(
        uploaded_by=request.user
    )

    user_comments = Comment.objects.filter(
        author=request.user
    )

    user_grave_suggestions = EditSuggestion.objects.filter(
        suggested_by=request.user
    )

    user_person_suggestions = PersonEditSuggestion.objects.filter(
        suggested_by=request.user
    )

    user_location_suggestions = LocationSuggestion.objects.filter(
        suggested_by=request.user
    )


    # -------------------------------------------------
    # GROBNI ZAPISI
    # -------------------------------------------------

    grave_count = user_graves.count()

    grave_approved = user_graves.filter(
        status=Grave.STATUS_APPROVED
    ).count()

    grave_pending = user_graves.filter(
        status=Grave.STATUS_PENDING
    ).count()

    grave_rejected = user_graves.filter(
        status=Grave.STATUS_REJECTED
    ).count()


    # -------------------------------------------------
    # OSOBE
    # -------------------------------------------------

    person_count = user_persons.count()

    person_approved = user_persons.filter(
        status=Person.STATUS_APPROVED
    ).count()

    person_pending = user_persons.filter(
        status=Person.STATUS_PENDING
    ).count()

    person_rejected = user_persons.filter(
        status=Person.STATUS_REJECTED
    ).count()


    # -------------------------------------------------
    # FOTOGRAFIJE
    # grobovi + groblja
    # -------------------------------------------------

    photo_count = (
        user_grave_photos.count()
        + user_cemetery_photos.count()
    )

    photo_approved = (
        user_grave_photos.filter(
            status=Photo.STATUS_APPROVED
        ).count()
        +
        user_cemetery_photos.filter(
            status=CemeteryPhoto.STATUS_APPROVED
        ).count()
    )

    photo_pending = (
        user_grave_photos.filter(
            status=Photo.STATUS_PENDING
        ).count()
        +
        user_cemetery_photos.filter(
            status=CemeteryPhoto.STATUS_PENDING
        ).count()
    )

    photo_rejected = (
        user_grave_photos.filter(
            status=Photo.STATUS_REJECTED
        ).count()
        +
        user_cemetery_photos.filter(
            status=CemeteryPhoto.STATUS_REJECTED
        ).count()
    )


    # -------------------------------------------------
    # KOMENTARI
    # -------------------------------------------------

    comment_count = user_comments.count()

    comment_approved = user_comments.filter(
        status=Comment.STATUS_APPROVED
    ).count()

    comment_pending = user_comments.filter(
        status=Comment.STATUS_PENDING
    ).count()

    comment_rejected = user_comments.filter(
        status=Comment.STATUS_REJECTED
    ).count()


    # -------------------------------------------------
    # PRIJEDLOZI IZMJENA
    # grob + osoba + lokacija
    # -------------------------------------------------

    suggestion_count = (
        user_grave_suggestions.count()
        + user_person_suggestions.count()
        + user_location_suggestions.count()
    )

    suggestion_approved = (
        user_grave_suggestions.filter(
            status=EditSuggestion.STATUS_APPROVED
        ).count()
        +
        user_person_suggestions.filter(
            status=PersonEditSuggestion.STATUS_APPROVED
        ).count()
        +
        user_location_suggestions.filter(
            approved=True
        ).count()
    )

    suggestion_pending = (
        user_grave_suggestions.filter(
            status=EditSuggestion.STATUS_PENDING
        ).count()
        +
        user_person_suggestions.filter(
            status=PersonEditSuggestion.STATUS_PENDING
        ).count()
        +
        user_location_suggestions.filter(
            approved=False
        ).count()
    )

    suggestion_rejected = (
        user_grave_suggestions.filter(
            status=EditSuggestion.STATUS_REJECTED
        ).count()
        +
        user_person_suggestions.filter(
            status=PersonEditSuggestion.STATUS_REJECTED
        ).count()
    )


    # -------------------------------------------------
    # UKUPNO
    # -------------------------------------------------

    total_contributions = (
        grave_count
        + person_count
        + photo_count
        + comment_count
        + suggestion_count
    )


    return render(
        request,
        "graves/profile.html",
        {
            "grave_count": grave_count,
            "grave_approved": grave_approved,
            "grave_pending": grave_pending,
            "grave_rejected": grave_rejected,

            "person_count": person_count,
            "person_approved": person_approved,
            "person_pending": person_pending,
            "person_rejected": person_rejected,

            "photo_count": photo_count,
            "photo_approved": photo_approved,
            "photo_pending": photo_pending,
            "photo_rejected": photo_rejected,

            "comment_count": comment_count,
            "comment_approved": comment_approved,
            "comment_pending": comment_pending,
            "comment_rejected": comment_rejected,

            "suggestion_count": suggestion_count,
            "suggestion_approved": suggestion_approved,
            "suggestion_pending": suggestion_pending,
            "suggestion_rejected": suggestion_rejected,

            "total_contributions": total_contributions,
        },
    )
    
@login_required
def add_comment(request, pk):
    grave = get_object_or_404(
        Grave,
        pk=pk,
        status=Grave.STATUS_APPROVED
    )

    if request.method == "POST":
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.grave = grave
            comment.author = request.user
            comment.status = Comment.STATUS_PENDING
            comment.save()

    return redirect("graves:grave_detail", pk=grave.id)


@login_required
def suggest_grave_edit(request, pk):
    grave = get_object_or_404(
        Grave,
        pk=pk,
        status=Grave.STATUS_APPROVED
    )

    if request.method == "POST":
        form = EditSuggestionForm(request.POST)

        if form.is_valid():
            suggestion = form.save(commit=False)
            suggestion.grave = grave
            suggestion.suggested_by = request.user

            field_name = suggestion.field_name
            suggestion.old_value = str(getattr(grave, field_name, ""))

            suggestion.save()

            return redirect("graves:grave_detail", pk=grave.id)

    else:
        form = EditSuggestionForm()

    return render(request, "graves/suggest_grave_edit.html", {
        "form": form,
        "grave": grave,
    })

@login_required
def suggest_grave_location(request, pk):

    grave = get_object_or_404(
        Grave.objects.select_related("cemetery"),
        pk=pk,
        status=Grave.STATUS_APPROVED,
    )

    if request.method == "POST":

        form = LocationSuggestionForm(request.POST)

        if form.is_valid():

            suggestion = form.save(commit=False)

            suggestion.grave = grave
            suggestion.suggested_by = request.user
            suggestion.approved = False

            suggestion.save()

            return redirect(
                "graves:grave_detail",
                pk=grave.pk,
            )

    else:

        initial = {}

        if grave.location:
            initial = {
                "latitude": grave.location.y,
                "longitude": grave.location.x,
            }

        form = LocationSuggestionForm(
            initial=initial
        )

    return render(
        request,
        "graves/suggest_grave_location.html",
        {
            "form": form,
            "grave": grave,
            "maptiler_api_key": settings.MAPTILER_API_KEY,
        },
    )


@login_required
def suggest_person_edit(request, pk):

    person = get_object_or_404(
        Person.objects.select_related(
            "grave",
            "grave__cemetery",
        ),
        pk=pk,
        status=Person.STATUS_APPROVED,
        grave__status=Grave.STATUS_APPROVED,
    )

    if request.method == "POST":

        form = PersonEditSuggestionForm(request.POST)

        if form.is_valid():

            suggestion = form.save(commit=False)

            suggestion.person = person
            suggestion.suggested_by = request.user

            field_name = suggestion.field_name

            old_value = getattr(
                person,
                field_name,
                "",
            )

            suggestion.old_value = (
                ""
                if old_value is None
                else str(old_value)
            )

            suggestion.save()

            return redirect(
                "graves:grave_detail",
                pk=person.grave.id,
            )

    else:

        form = PersonEditSuggestionForm()

    return render(
        request,
        "graves/suggest_person_edit.html",
        {
            "form": form,
            "person": person,
            "grave": person.grave,
        },
    )


def statistics(request):

    stats = {
        "cemetery_count": Cemetery.objects.filter(status=Cemetery.STATUS_APPROVED).count(),

        "grave_count": Grave.objects.filter(
            status=Grave.STATUS_APPROVED,
            cemetery__status=Cemetery.STATUS_APPROVED,
        ).count(),

        "person_count": Person.objects.filter(
            status=Person.STATUS_APPROVED,
            grave__status=Grave.STATUS_APPROVED,
            grave__cemetery__status=Cemetery.STATUS_APPROVED,
        ).count(),

        "photo_count": Photo.objects.filter(
            status=Photo.STATUS_APPROVED,
            grave__status=Grave.STATUS_APPROVED,
            grave__cemetery__status=Cemetery.STATUS_APPROVED,
        ).count(),

        "user_count": User.objects.count(),
    }

    return render(
        request,
        "graves/statistics.html",
        {
            "stats": stats,
        },
    )

    return render(request, "graves/statistics.html", {
        "stats": stats,
    })

def person_list(request):
    query = request.GET.get("q", "").strip()
    birth_year = request.GET.get("birth_year", "").strip()
    death_year = request.GET.get("death_year", "").strip()

    show_all = request.GET.get("show_all") == "1"

    has_search = bool(
        query or
        birth_year or
        death_year or
        show_all
    )

    persons = Person.objects.none()

    if has_search:

        persons = Person.objects.select_related(
            "grave",
            "grave__cemetery"
        ).filter(
            grave__status=Grave.STATUS_APPROVED,
            grave__cemetery__status=Cemetery.STATUS_APPROVED,
            status=Person.STATUS_APPROVED,
        )

        if query:
            persons = persons.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )

        if birth_year.isdigit():
            persons = persons.filter(
                birth_year=int(birth_year)
            )

        if death_year.isdigit():
            persons = persons.filter(
                death_year=int(death_year)
            )

        persons = persons.order_by(
            "last_name",
            "first_name",
            "birth_year"
        )

    paginator = Paginator(persons, 20)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "graves/person_list.html",
        {
            "persons": page_obj,
            "page_obj": page_obj,
            "query": query,
            "birth_year": birth_year,
            "death_year": death_year,
            "show_all": show_all,
            "has_search": has_search,
            "result_count": paginator.count,
        }
    )

def surname_list(request):
    query = request.GET.get("q", "").strip()

    surnames = (
        Person.objects
        .filter(grave__status=Grave.STATUS_APPROVED,
            grave__cemetery__status=Cemetery.STATUS_APPROVED,
            status=Person.STATUS_APPROVED, 
            is_unknown=False,)
        .exclude(last_name="")
        .exclude(
            Q(last_name__iexact="nepoznat") |
            Q(last_name__iexact="nepoznata") |
            Q(last_name__iexact="nepoznato") |
            Q(last_name__iexact="nn") |
            Q(last_name__iexact="n.n.") |
            Q(last_name__iexact="nije poznato")
        )
        .values("last_name")
        .annotate(total=Count("id"))
    )

    if query:
        surnames = surnames.filter(
            last_name__icontains=query
        )

    surnames = surnames.order_by("last_name")

    paginator = Paginator(
        surnames,
        12,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "graves/surname_list.html",
        {
            "surnames": page_obj,
            "page_obj": page_obj,
            "query": query,
            "result_count": paginator.count,
        },
    )


def surname_detail(request, last_name):

    persons = (
        Person.objects
        .filter(
            last_name__iexact=last_name,
            grave__status=Grave.STATUS_APPROVED,
            grave__cemetery__status=Cemetery.STATUS_APPROVED,
            status=Person.STATUS_APPROVED,
            is_unknown=False,
        )
        .select_related(
            "grave",
            "grave__cemetery"
        )
        .order_by(
            "death_year",
            "birth_year",
            "first_name"
        )
    )

    cemeteries = (
        persons
        .values(
            "grave__cemetery__id",
            "grave__cemetery__name",
        )
        .annotate(
            person_count=Count("id")
        )
        .order_by(
            "grave__cemetery__name"
        )
    )

    cemetery_list = [
        {
            "id": item["grave__cemetery__id"],
            "name": item["grave__cemetery__name"],
            "person_count": item["person_count"],
        }
        for item in cemeteries
    ]

    return render(
        request,
        "graves/surname_detail.html",
        {
            "last_name": last_name,
            "persons": persons,
            "cemeteries": cemetery_list,
        },
    )

def contributors(request):

    users = (
        User.objects
        .annotate(
            grave_count=Count(
                "grave",
                filter=Q(
                    grave__status=Grave.STATUS_APPROVED
                ),
                distinct=True,
            ),

            person_count=Count(
                "created_persons",
                filter=Q(
                    created_persons__status=Person.STATUS_APPROVED
                ),
                distinct=True,
            ),

            grave_photo_count=Count(
                "photo",
                filter=Q(
                    photo__status=Photo.STATUS_APPROVED
                ),
                distinct=True,
            ),

            cemetery_photo_count=Count(
                "cemeteryphoto",
                filter=Q(
                    cemeteryphoto__status=CemeteryPhoto.STATUS_APPROVED
                ),
                distinct=True,
            ),

            grave_edit_count=Count(
                "editsuggestion",
                filter=Q(
                    editsuggestion__status=EditSuggestion.STATUS_APPROVED
                ),
                distinct=True,
            ),

            person_edit_count=Count(
                "personeditsuggestion",
                filter=Q(
                    personeditsuggestion__status=
                    PersonEditSuggestion.STATUS_APPROVED
                ),
                distinct=True,
            ),

            location_suggestion_count=Count(
                "locationsuggestion",
                filter=Q(
                    locationsuggestion__approved=True
                ),
                distinct=True,
            ),
        )
    )

    for user in users:

        user.photo_count = (
            user.grave_photo_count +
            user.cemetery_photo_count
        )

        user.edit_count = (
            user.grave_edit_count +
            user.person_edit_count +
            user.location_suggestion_count
        )

        user.contribution_count = (
            user.grave_count +
            user.person_count +
            user.photo_count +
            user.edit_count
        )

        if user.contribution_count >= 100:
            user.contribution_level = "gold"

        elif user.contribution_count >= 50:
            user.contribution_level = "silver"

        elif user.contribution_count >= 10:
            user.contribution_level = "bronze"

        else:
            user.contribution_level = None
            
    users = [
        user
        for user in users
        if user.contribution_count > 0
    ]

    users.sort(
        key=lambda user: user.contribution_count,
        reverse=True,
    )

    total_graves = sum(
        user.grave_count
        for user in users
    )

    total_persons = sum(
        user.person_count
        for user in users
    )

    total_photos = sum(
        user.photo_count
        for user in users
    )

    total_edits = sum(
        user.edit_count
        for user in users
    )

    total_contributions = sum(
        user.contribution_count
        for user in users
    )

    context = {
        "users": users,
        "total_graves": total_graves,
        "total_persons": total_persons,
        "total_photos": total_photos,
        "total_edits": total_edits,
        "total_contributions": total_contributions
    }

    return render(
        request,
        "graves/contributors.html",
        context,
    )

@login_required
def report_problem(request, pk):
    grave = get_object_or_404(
        Grave,
        pk=pk,
        status=Grave.STATUS_APPROVED
    )

    if request.method == "POST":
        form = ProblemReportForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.grave = grave
            report.reported_by = request.user
            report.status = ProblemReport.STATUS_OPEN
            report.save()

            return redirect("graves:grave_detail", pk=grave.id)

    else:
        form = ProblemReportForm()

    return render(request, "graves/report_problem.html", {
        "form": form,
        "grave": grave,
    })
reader = easyocr.Reader(
    ['en', 'hr'],
    gpu=False
)

@staff_member_required
def photo_ocr(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":

        EditSuggestion.objects.create(
            grave=photo.grave,
            suggested_by=request.user,
            field_name="inscription",
            old_value=photo.grave.inscription or "",
            new_value=request.POST.get("ocr_text", ""),
        )

        return redirect(
            "graves:grave_detail",
            pk=photo.grave.id
        )
        
    text = ""

    try:
        image_path = photo.image.path
        image = Image.open(image_path)

        results = reader.readtext(image_path)

        text = "\n".join([result[1] for result in results])    

    except Exception as e:
        text = f"OCR greška: {e}"

    return render(request, "graves/photo_ocr.html", {
        "photo": photo,
        "text": text,
    })
    
@require_POST
def ocr_inscription(request):
    image = request.FILES.get("image")

    if not image:
        return JsonResponse(
            {
                "success": False,
                "error": "Fotografija nije poslana.",
            },
            status=400,
        )

    try:
        text = recognize_inscription(image)

        return JsonResponse(
            {
                "success": True,
                "text": text,
            }
        )

    except Exception as exc:
        print(f"OCR error: {exc}")

        return JsonResponse(
            {
                "success": False,
                "error": "Fotografiju nije bilo moguće obraditi.",
            },
            status=500,
        )
