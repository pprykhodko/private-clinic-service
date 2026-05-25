from django.contrib.auth.models import AbstractUser
from django.db import models


class Doctor(AbstractUser):
    specialization = models.CharField(max_length=255)
    years_of_experience = models.PositiveIntegerField(default=0)
    patients = models.ManyToManyField(
        "Patient",
        through="Appointment",
        related_name="doctors"
    )

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.specialization})"


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    appointment_date = models.DateTimeField()
    notes = models.TextField(max_length=255, blank=True, default="-")

    class Meta:
        ordering = ["appointment_date"]

    def __str__(self):
        return f"({self.appointment_date:%d.%m.%Y}) {self.patient}"


class CTScan(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="ct_scans"
    )
    scan_date = models.DateTimeField()
    description = models.TextField(max_length=255, blank=True, default="-")

    class Meta:
        ordering = ["scan_date"]

    def __str__(self):
        return f"CT Scan #{self.id} - {self.patient}"
