from django import forms
from django.core.exceptions import ValidationError
from booking.models import Booking, TrainerAvailability
from datetime import datetime

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'trainer', 'service', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        """Custom validation for trainer availability before saving."""
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')
        booking_date = cleaned_data.get('date')
        booking_time = cleaned_data.get('time')

        if trainer and booking_date and booking_time:
            try:
                availability = trainer.availabilities  # Get trainer's availability
            except TrainerAvailability.DoesNotExist:
                raise ValidationError("This trainer does not have availability set up.")

            weekday = booking_date.strftime('%A').lower()  # Convert date to weekday
            available = getattr(availability, weekday, False)  # Check if available that day
            start_time = getattr(availability, f"{weekday}_start", None)
            end_time = getattr(availability, f"{weekday}_end", None)

            # Check if trainer is available on that day
            if not available or not start_time or not end_time:
                raise ValidationError(f"{trainer.user.username} is not available on {weekday.capitalize()}.")

            # Check if the booking time is within working hours
            if not (start_time <= booking_time <= end_time):
                raise ValidationError(f"Booking time must be between {start_time} and {end_time} on {weekday.capitalize()}.")

        return cleaned_data
