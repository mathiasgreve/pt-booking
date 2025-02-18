from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

class MyUser(AbstractUser):
    email = models.EmailField(_('email address'), unique = True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    is_admin = models.BooleanField(default=False)
    is_trainer = models.BooleanField(default=False)  # Marks trainers
 

    def __str__(self):
        return self.username


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")  # Duration of the treatment in minutes
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    image = models.ImageField(upload_to='treatment_images/', blank=True, null=True)  # Add this
    image_url = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.duration_minutes} min)"


class Trainer(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    
    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return self.user.username
    
class TrainerAvailability(models.Model):
    trainer = models.OneToOneField(Trainer, on_delete=models.CASCADE, related_name='availabilities', unique=True)
    
    monday = models.BooleanField(default=False)
    monday_start = models.TimeField(blank=True, null=True)
    monday_end = models.TimeField(blank=True, null=True)
    
    tuesday = models.BooleanField(default=False)
    tuesday_start = models.TimeField(blank=True, null=True)
    tuesday_end = models.TimeField(blank=True, null=True)

    wednesday = models.BooleanField(default=False)
    wednesday_start = models.TimeField(blank=True, null=True)
    wednesday_end = models.TimeField(blank=True, null=True)

    thursday = models.BooleanField(default=False)
    thursday_start = models.TimeField(blank=True, null=True)
    thursday_end = models.TimeField(blank=True, null=True)

    friday = models.BooleanField(default=False)
    friday_start = models.TimeField(blank=True, null=True)
    friday_end = models.TimeField(blank=True, null=True)

    saturday = models.BooleanField(default=False)
    saturday_start = models.TimeField(blank=True, null=True)
    saturday_end = models.TimeField(blank=True, null=True)

    sunday = models.BooleanField(default=False)
    sunday_start = models.TimeField(blank=True, null=True)
    sunday_end = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Availability for {self.trainer.user.username}"

class AvailabilityException(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="availability_exceptions")
    date = models.DateField()
    is_available = models.BooleanField(default=True)  # False = not available
    start_time = models.TimeField(blank=True, null=True)  # Optional custom time
    end_time = models.TimeField(blank=True, null=True)  # Optional custom time

    def __str__(self):
        status = "Available" if self.is_available else "Not Available"
        return f"{self.trainer.user.username} - {status} on {self.date}"


class Booking(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, related_name="trainer_bookings")
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)  # End time (calculated)

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="pending",
    )
    
    def clean(self):
        """Validate if the booking time falls within the trainer's availability and prevent duplicate bookings."""
        # Ensure trainer has availability set
        try:
            availability = self.trainer.availabilities
        except TrainerAvailability.DoesNotExist:
            raise ValidationError("This trainer does not have availability set up.")

        # Get the day of the week
        weekday = self.date.strftime('%A').lower()

        # Check if trainer is available on that day
        available = getattr(availability, weekday, False)
        start_time = getattr(availability, f"{weekday}_start", None)
        end_time = getattr(availability, f"{weekday}_end", None)

        if not available or not start_time or not end_time:
            raise ValidationError(f"{self.trainer.user.username} is not available on {weekday.capitalize()}.")
        
        # Calculate `end_time` using service duration
        if self.service and self.service.duration_minutes:
            self.end_time = (datetime.combine(self.date, self.time) + timedelta(minutes=self.service.duration_minutes)).time()
        else:
            raise ValidationError("Service duration must be set.")

        # Check if booking time is within trainer's working hours. NB this will go past the trainer's end_time for the day 
        if not (start_time <= self.time <= end_time):
            raise ValidationError(f"Booking time must be between {start_time} and {end_time} on {weekday.capitalize()}.")

        #  Prevent double/overlapping bookings at the same time 
        overlapping_booking = Booking.objects.filter(
            trainer=self.trainer, 
            date=self.date
        ).exclude(id=self.id).filter(  # Exclude current booking when updating
            models.Q(time__lt=self.end_time, end_time__gt=self.time)
        )

        if overlapping_booking.exists():
            raise ValidationError("This trainer already has a booking that overlaps with this time.")

    def save(self, *args, **kwargs):
        """Ensure validation runs before saving."""
        self.clean()  # Run validation
        super().save(*args, **kwargs)  # Proceed with saving

    def __str__(self):
        return f"Booking for {self.user.username} on {self.date} at {self.time}"