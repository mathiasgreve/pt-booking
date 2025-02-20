from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainerAvailability, Booking, Service, Trainer
from booking.models import Service, Booking
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse

navbarContent = [
    {"url_name": "pt_presentation:hjem", "base_name": "hjem", "display_name": "Hjem"},
    {"url_name": "pt_presentation:om_meg", "base_name": "om_meg", "display_name": "Om meg"},
    {"url_name": "pt_presentation:blog", "base_name": "blog", "display_name": "Blog"},
    {"url_name": "pt_presentation:treningsfilosofi", "base_name": "treningsfilosofi", "display_name": "Treningsfilosofi"},
    {"url_name": "pt_presentation:ernaering", "base_name": "ernaering", "display_name": "Ernæring"},
]

# Create your views here.
def services(request):
    pt_services = Service.objects.all()

    data = {
        "pt_services": pt_services,
        "navbarContent": navbarContent
    }

    return render(request, "booking/services.html", data)

def booking(request, service_id):
    trainer = Trainer.objects.first().name
    data = {
        "navbarContent": navbarContent,
        "service_id": service_id,
        "trainer": trainer,
    }
    return render(request, "booking/booking.html", data)

def available_dates(request):
    # Fetch available dates
    available_dates = Booking.objects.values_list('date', flat=True).distinct()
    return JsonResponse([str(date) for date in available_dates], safe=False)

def available_times(request):
    date_str = request.GET.get('date')
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    
    trainer = TrainerAvailability.objects.first()  # Example: Get first trainer
    weekday = date.strftime('%A').lower()

    if not getattr(trainer, weekday):
        return JsonResponse({"times": []})  # Trainer not available on that weekday

    start_time = getattr(trainer, f"{weekday}_start")
    end_time = getattr(trainer, f"{weekday}_end")

    times = []
    current_time = start_time
    while current_time < end_time:
        times.append(current_time.strftime("%H:%M"))
        current_time = (datetime.combine(date, current_time) + timedelta(minutes=30)).time()

    booked_times = Booking.objects.filter(date=date).values_list('time', flat=True)
    available_times = [t for t in times if t not in booked_times]

    return JsonResponse({"times": available_times})
