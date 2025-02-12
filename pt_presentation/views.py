from django.shortcuts import render
from django.http import HttpResponse

# navbarContent = [
#     {"url_name":"hjem", "display_name": "Hjem"},
#     {"url_name":"om_meg", "display_name": "Om meg"},
#     {"url_name":"blog", "display_name": "Blog"},
#     {"url_name":"treningsfilosofi", "display_name": "Treningsfilosofi"},
#     {"url_name":"ernaering", "display_name": "Ernæring"},
#     ]

navbarContent = [
    {"url_name": "pt_presentation:hjem", "base_name": "hjem", "display_name": "Hjem"},
    {"url_name": "pt_presentation:om_meg", "base_name": "om_meg", "display_name": "Om meg"},
    {"url_name": "pt_presentation:blog", "base_name": "blog", "display_name": "Blog"},
    {"url_name": "pt_presentation:treningsfilosofi", "base_name": "treningsfilosofi", "display_name": "Treningsfilosofi"},
    {"url_name": "pt_presentation:ernaering", "base_name": "ernaering", "display_name": "Ernæring"},
]

def hjem(request):
    return render(request, "frontpage/hjem.html", {
        "navbarContent": navbarContent
    })

def om_meg(request):
    return render(request, "frontpage/om_meg.html", {
        "navbarContent": navbarContent
    })

def blog(request):
    return render(request, "frontpage/blog.html", {
        "navbarContent": navbarContent
    })

def treningsfilosofi(request):
    return render(request, "frontpage/treningsfilosofi.html", {
        "navbarContent": navbarContent
    })

def ernæring(request):
    return render(request, "frontpage/ernaering.html", {
        "navbarContent": navbarContent
    })