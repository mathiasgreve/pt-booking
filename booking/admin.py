from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Booking, Service, Trainer, TrainerAvailability, AvailabilityException
from django import forms

# Simple registration
admin.site.register(MyUser)
admin.site.register(Trainer)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(TrainerAvailability)
admin.site.register(AvailabilityException)
