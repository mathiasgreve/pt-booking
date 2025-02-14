from django.contrib import admin
from .models import Profile, Booking, Service, Trainer, DaysNotWorking

# Simple registration
admin.site.register(Profile)
admin.site.register(Service)

# Customize the admin interface for complex models like Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'service', 'trainer', 'time', 'date')  # Fields shown in the admin list view
    list_filter = ('trainer', 'date')  # Add filters on the side
    search_fields = ('user__username', 'trainer__name')  # Enable search for related fields

@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('name', 'available_times')
    search_fields = ('name',)

@admin.register(DaysNotWorking)
class DaysNotWorkingAdmin(admin.ModelAdmin):
    list_display = ('trainer', 'start_date', 'end_date')
    list_filter = ('trainer',)