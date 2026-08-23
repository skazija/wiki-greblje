from .models import (
    Grave,
    Person,
    Photo,
    CemeteryPhoto,
    EditSuggestion,
    PersonEditSuggestion,
    LocationSuggestion,
    Comment,
    ProblemReport,
)


def pending_admin_items(request):

    if not (
        request.user.is_authenticated
        and request.user.is_staff
    ):
        return {
            "has_pending_admin_items": False
        }

    has_pending = (
        Grave.objects.filter(
            status=Grave.STATUS_PENDING
        ).exists()

        or Person.objects.filter(
            status=Person.STATUS_PENDING
        ).exists()

        or Photo.objects.filter(
            status=Photo.STATUS_PENDING
        ).exists()

        or CemeteryPhoto.objects.filter(
            status=CemeteryPhoto.STATUS_PENDING
        ).exists()

        or Comment.objects.filter(
            status=Comment.STATUS_PENDING
        ).exists()

        or EditSuggestion.objects.filter(
            status=EditSuggestion.STATUS_PENDING
        ).exists()

        or PersonEditSuggestion.objects.filter(
            status=PersonEditSuggestion.STATUS_PENDING
        ).exists()

        or LocationSuggestion.objects.filter(
            approved=False
        ).exists()

        or ProblemReport.objects.filter(
            status=ProblemReport.STATUS_OPEN
        ).exists()
    )

    return {
        "has_pending_admin_items": has_pending
    }