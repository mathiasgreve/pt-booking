from django.urls import path
from . import views

app_name = 'booking'
urlpatterns = [
    path("", views.services, name="services"),
    path("booking/", views.booking, name="booking")
]