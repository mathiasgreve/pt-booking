from django.urls import path, include
from . import views

app_name="pt_presentation"
urlpatterns = [
    path("hjem/", views.hjem, name="hjem"),
    path("om-meg/", views.om_meg, name="om_meg"),
    path("blog/", views.blog, name="blog"),
    path("ernaering/", views.ernæring, name="ernaering"),
    path("treningsfilosofi/", views.treningsfilosofi, name="treningsfilosofi"),
    # path("appointment/", include("appointment.urls")),
]