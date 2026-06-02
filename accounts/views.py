from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

from django import forms
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required
from django.db.models import Count


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Korisničko ime",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password1 = forms.CharField(
        label="Lozinka",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    password2 = forms.CharField(
        label="Potvrda lozinke",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")



def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect("/")

    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {
        "form": form
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
