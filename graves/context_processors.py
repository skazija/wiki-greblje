from .models import Grave


def pending_graves_count(request):
    if request.user.is_authenticated and request.user.is_staff:
        count = Grave.objects.filter(
            status=Grave.STATUS_PENDING
        ).count()
    else:
        count = 0

    return {
        "pending_graves_count": count
    }