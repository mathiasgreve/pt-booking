from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainerAvailability, Booking, Service, Trainer
from booking.models import Service, Booking, MyUser
from datetime import datetime, timedelta
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

    if not date_str:
        return JsonResponse({"success": False, "error": "Date is required!"})

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Convert string to date object
    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid date format!"})
    
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

    # Fetch booked times and convert them to string format
    booked_times = Booking.objects.filter(date=date).values_list('time', flat=True)
    booked_times = [bt.strftime("%H:%M") for bt in booked_times]  # Convert to string format

    # Remove booked times from available slots
    available_times = [t for t in times if t not in booked_times]

    return JsonResponse({"times": available_times})


def create_booking(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            date_str = data.get("date")  
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = data.get("time")
            additional_info = data.get("additional_info", "")
            service_id = data.get("service_id")  # Get service_id from request

            if not service_id:
                return JsonResponse({"success": False, "error": "Service ID missing!"})

            # Convert time string to a valid TimeField format
            time_obj = datetime.strptime(time, "%H:%M").time()

            # Fetch the service
            service = Service.objects.get(id=service_id)  # Fix here

            # Assign a trainer (modify as needed)
            trainer = Trainer.objects.first()
            user = request.user  # Ensure the user is authenticated

            # Create booking
            booking = Booking.objects.create(
                user=user,
                trainer=trainer,
                service=service,
                date=date,
                time=time_obj
            )

            return JsonResponse({"success": True, "booking_id": booking.id})

        except Service.DoesNotExist:
            return JsonResponse({"success": False, "error": "Service not found!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})
