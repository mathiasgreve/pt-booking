from django.shortcuts import render
from appointment.models import Service

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
    return render(request, "booking/booking.html", {
        "pt_services": pt_services,
        "navbarContent": navbarContent
    })