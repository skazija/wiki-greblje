import os
import easyocr
import pytesseract
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
from .models import EditSuggestion    
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Cemetery, Grave, Person, Photo, EditSuggestion, Comment, ProblemReport

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .forms import PublicGraveForm, EditSuggestionForm, CommentForm, ProblemReportForm
from django.http import JsonResponse

from django.db.models import Count
from django.http import Http404

from django.contrib.auth.models import User
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D

from django.contrib.admin.views.decorators import staff_member_required

from PIL import Image
from .models import Photo


def cemetery_list(request):
    cemeteries = Cemetery.objects.all().order_by("name")

    return render(request, "graves/cemetery_list.html", {
        "cemeteries": cemeteries,
    })


def cemetery_detail(request, pk):
    cemetery = get_object_or_404(Cemetery, pk=pk)
    graves = cemetery.graves.filter(status=Grave.STATUS_APPROVED).prefetch_related("persons", "photos")

    return render(request, "graves/cemetery_detail.html", {
        "cemetery": cemetery,
        "graves": graves,
    })


def grave_detail(request, pk):

    grave = get_object_or_404(Grave, pk=pk)

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

    last_names = grave.persons.exclude(
        last_name=""
    ).values_list(
        "last_name",
        flat=True
    ).distinct()

    if last_names:
        related_persons = Person.objects.filter(
            last_name__in=last_names,
            grave__status=Grave.STATUS_APPROVED
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

    return render(request, "graves/grave_detail.html", {
        "grave": grave,
        "edit_history": edit_history,
        "related_persons": related_persons,
        "comments": comments,
        "comment_form": comment_form,
        "nearby_graves": nearby_graves,
    })


def search(request):
    query = request.GET.get("q", "").strip()

    graves = Grave.objects.none()
    persons = Person.objects.none()
    map_graves = []

    
    if query:
        graves = Grave.objects.filter(
            Q(title__icontains=query) |
            Q(inscription__icontains=query) |
            Q(notes__icontains=query) |
            Q(cemetery__name__icontains=query),
            status=Grave.STATUS_APPROVED
        ).select_related("cemetery")

        persons = Person.objects.filter(grave__status=Grave.STATUS_APPROVED).filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(birth_date_text__icontains=query) |
            Q(death_date_text__icontains=query) |
            Q(notes__icontains=query)
        ).select_related("grave", "grave__cemetery")

        grave_ids = set()

        for grave in graves:
            if grave.location and grave.id not in grave_ids:
                grave_ids.add(grave.id)
                map_graves.append(grave)

        for person in persons:
            grave = person.grave
            if grave.location and grave.id not in grave_ids:
                grave_ids.add(grave.id)
                map_graves.append(grave)

    return render(request, "graves/search.html", {
        "query": query,
        "graves": graves,
        "persons": persons,
        "map_graves": map_graves,
    })

def home(request):
    cemetery_count = Cemetery.objects.count()
    grave_count = Grave.objects.count()
    person_count = Person.objects.count()
    photo_count = Photo.objects.count()
    user_count = User.objects.count()

    latest_graves = Grave.objects.prefetch_related(
        "photos",
        "persons"
    ).order_by("-created_at")[:6]

    latest_photos = Photo.objects.select_related(
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
def add_grave(request):
    if request.method == "POST":
        form = PublicGraveForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            grave = form.save(user=request.user)

            return redirect("graves:my_graves")
    else:
        form = PublicGraveForm()

    return render(request, "graves/add_grave.html", {
        "form": form,
    })

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
    cemetery = get_object_or_404(Cemetery, pk=pk)

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

    total_graves = user_graves.count()

    approved_graves = user_graves.filter(
        status=Grave.STATUS_APPROVED
    ).count()

    pending_graves = user_graves.filter(
        status=Grave.STATUS_PENDING
    ).count()

    return render(request, "graves/profile.html", {
        "total_graves": total_graves,
        "approved_graves": approved_graves,
        "pending_graves": pending_graves,
    })

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

def statistics(request):
    stats = {
        "cemetery_count": Cemetery.objects.count(),
        "grave_count": Grave.objects.count(),
        "approved_grave_count": Grave.objects.filter(
            status=Grave.STATUS_APPROVED
        ).count(),
        "pending_grave_count": Grave.objects.filter(
            status=Grave.STATUS_PENDING
        ).count(),
        "rejected_grave_count": Grave.objects.filter(
            status=Grave.STATUS_REJECTED
        ).count(),
        "person_count": Person.objects.count(),
        "photo_count": Photo.objects.count(),
        "user_count": User.objects.count(),
        "edit_suggestion_count": EditSuggestion.objects.count(),
        "pending_edit_suggestion_count": EditSuggestion.objects.filter(
            status=EditSuggestion.STATUS_PENDING
        ).count(),
    }

    return render(request, "graves/statistics.html", {
        "stats": stats,
    })

def person_list(request):
    query = request.GET.get("q", "").strip()
    birth_year = request.GET.get("birth_year", "").strip()
    death_year = request.GET.get("death_year", "").strip()

    persons = Person.objects.select_related(
        "grave",
        "grave__cemetery"
    ).filter(
        grave__status=Grave.STATUS_APPROVED
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

    persons = persons.order_by("last_name", "first_name")

    return render(request, "graves/person_list.html", {
        "persons": persons,
        "query": query,
        "birth_year": birth_year,
        "death_year": death_year,
    })

def surname_list(request):
    query = request.GET.get("q", "").strip()

    surnames = (
        Person.objects
        .filter(grave__status=Grave.STATUS_APPROVED)
        .exclude(last_name="")
        .values("last_name")
        .annotate(total=Count("id"))
    )

    if query:
        surnames = surnames.filter(
            last_name__icontains=query
        )

    surnames = surnames.order_by("last_name")

    return render(request, "graves/surname_list.html", {
        "surnames": surnames,
        "query": query,
    })


def surname_detail(request, last_name):
    persons = (
        Person.objects
        .filter(
            last_name__iexact=last_name,
            grave__status=Grave.STATUS_APPROVED
        )
        .select_related("grave", "grave__cemetery")
        .order_by("death_year", "birth_year", "first_name")
    )
    map_graves = []

    for person in persons:
        if person.grave.location:
            map_graves.append({
                "id": person.grave.id,
                "title": str(person.grave),
                "lat": person.grave.location.y,
                "lng": person.grave.location.x,
                "cemetery": person.grave.cemetery.name,
            })

    return render(request, "graves/surname_detail.html", {
        "last_name": last_name,
        "persons": persons,
        "map_graves": map_graves,
    })

def contributors(request):

    users = User.objects.annotate(
        grave_count=Count("grave", distinct=True),
        comment_count=Count("comment", distinct=True),
    )

    users = users.order_by(
        "-grave_count",
        "-comment_count",
        "username",
    )

    return render(
        request,
        "graves/contributors.html",
        {
            "users": users,
        }
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