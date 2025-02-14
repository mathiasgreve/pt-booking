from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import gettext_lazy as _


# User Roles
class Profile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        TRAINER = 'trainer', _('Trainer')
        CUSTOMER = 'customer', _('Customer')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Service(models.Model):
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()  # Duration of the treatment in minutes
    image = models.ImageField(upload_to='treatment_images/', blank=True, null=True)  # Add this
    image_url = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    available_times = models.JSONField()  # Example: {"Monday": ["09:00", "10:00"], "Tuesday": ["14:00", "15:00"]}
    
    @property
    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def __str__(self):
        return self.user.username
    
class DaysNotWorking(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.trainer.user.username}: {self.start_date} to {self.end_date}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending')
        ACCEPTED = 'accepted', _('Accepted')
        DECLINED = 'declined', _('Declined')

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Booking for {self.user.username} with {self.trainer.user.username} on {self.date} at {self.time}"


class BookingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    servive = models.ForeignKey(Service, on_delete=models.CASCADE)
    requested_date = models.DateField()
    requested_time = models.TimeField()
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.username} for {self.service.name} on {self.requested_date} at {self.requested_time}"