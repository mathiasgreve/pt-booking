# Generated by Django 5.1.6 on 2025-02-18 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_booking_end_time_alter_service_duration_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
