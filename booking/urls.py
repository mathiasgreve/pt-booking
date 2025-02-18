from django.urls import path
from . import views
app_name = 'booking'
urlpatterns = [
    path("", views.services, name="services"),
    path("booking/", views.booking, name="booking"),
    path("api/available_dates/", views.AvailableDatesView.as_view(), name="available_dates"),
    path("api/available_times/", views.AvailableTimesView.as_view(), name="available_times"),
    path("api/book_session/", views.CreateBookingView.as_view(), name="book_session"),
]