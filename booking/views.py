from django.shortcuts import render
# from appointment.models import Service
from booking.models import Service

navbarContent = [
    {"url_name": "pt_presentation:hjem", "base_name": "hjem", "display_name": "Hjem"},
    {"url_name": "pt_presentation:om_meg", "base_name": "om_meg", "display_name": "Om meg"},
    {"url_name": "pt_presentation:blog", "base_name": "blog", "display_name": "Blog"},
    {"url_name": "pt_presentation:treningsfilosofi", "base_name": "treningsfilosofi", "display_name": "Treningsfilosofi"},
    {"url_name": "pt_presentation:ernaering", "base_name": "ernaering", "display_name": "Ernæring"},
]

# Create your views here.
def booking(request):
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

    return render(request, "booking/booking.html", data)