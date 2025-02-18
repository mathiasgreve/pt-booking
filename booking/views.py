from django.shortcuts import render
from .models import TrainerAvailability, Booking, Service
from booking.models import Service
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views import View


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

    # if request.user.profile.role == 'trainer':
    # # Show trainer-specific bookings
    #     pass
    # elif request.user.profile.role == 'customer':
    # # Show customer-specific bookings
    #     pass

    data = {
        "pt_services": pt_services,
        "navbarContent": navbarContent
    }

    return render(request, "booking/services.html", data)

def booking(request):
    data = {
        "navbarContent": navbarContent
    }
    return render(request, "booking/booking.html", data)


class AvailableDatesView(View):
    def get(self, request):
        """Get dates where at least one trainer is available."""
        available_dates = set()
        trainers = TrainerAvailability.objects.all()

        for trainer in trainers:
            for day, available in [
                ("monday", trainer.monday),
                ("tuesday", trainer.tuesday),
                ("wednesday", trainer.wednesday),
                ("thursday", trainer.thursday),
                ("friday", trainer.friday),
                ("saturday", trainer.saturday),
                ("sunday", trainer.sunday),
            ]:
                if available:
                    weekday_number = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(day)
                    date = datetime.today() + timedelta(days=(weekday_number - datetime.today().weekday()) % 7)
                    available_dates.add(date.strftime("%Y-%m-%d"))

        return JsonResponse({"available_dates": list(available_dates)})

class AvailableTimesView(View):
    def get(self, request):
        """Get available time slots for a selected date."""
        selected_date = request.GET.get("date")
        if not selected_date:
            return JsonResponse({"error": "Date is required"}, status=400)

        selected_day = datetime.strptime(selected_date, "%Y-%m-%d").strftime("%A").lower()
        available_times = []

        for trainer in TrainerAvailability.objects.all():
            if getattr(trainer, selected_day, False):
                start_time = getattr(trainer, f"{selected_day}_start")
                end_time = getattr(trainer, f"{selected_day}_end")
                
                # Generate time slots in 1-hour intervals
                current_time = start_time
                while current_time < end_time:
                    available_times.append(current_time.strftime("%H:%M"))
                    current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=60)).time()
        
        return JsonResponse({"available_times": available_times})

class CreateBookingView(View):
    def post(self, request):
        """Create a new booking."""
        import json
        data = json.loads(request.body)

        user_id = data.get("user_id")
        service_id = data.get("service_id")
        trainer_id = data.get("trainer_id")
        date = data.get("date")
        time = data.get("time")

        if not all([user_id, service_id, trainer_id, date, time]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        # Create booking
        booking = Booking.objects.create(
            user_id=user_id,
            service_id=service_id,
            trainer_id=trainer_id,
            date=date,
            time=time
        )
        return JsonResponse({"message": "Booking created", "booking_id": booking.id})