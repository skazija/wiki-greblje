from django.urls import path
from . import views

app_name = "graves"

urlpatterns = [
    path("", views.home, name="home"),
    path("groblja/", views.cemetery_list, name="cemetery_list"),
    path("groblja/<int:pk>/", views.cemetery_detail, name="cemetery_detail"),
    path("grobovi/<int:pk>/", views.grave_detail, name="grave_detail"),
    path("pretraga/", views.search, name="search"),
    path("dodaj-grob/", views.add_grave, name="add_grave"),
    path("moji-grobovi/", views.my_graves, name="my_graves"),
    path("api/cemetery-location/<int:pk>/", views.cemetery_location_api, name="cemetery_location_api",),
    path("moj-profil/", views.profile, name="profile"),
    path("grobovi/<int:pk>/predlozi-izmjenu/",views.suggest_grave_edit,name="suggest_grave_edit",),
    path("statistika/", views.statistics, name="statistics"),
    path("osobe/",views.person_list,name="person_list"),
    path("grobovi/<int:pk>/komentar/",views.add_comment,name="add_comment",),
    path("prezimena/", views.surname_list, name="surname_list"),
    path("prezimena/<str:last_name>/", views.surname_detail, name="surname_detail"),
    path("doprinosi/",views.contributors,name="contributors",),
]