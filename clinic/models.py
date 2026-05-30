from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe


name_validator = RegexValidator(
    regex=r"^[A-Za-zА-Яа-яІіЇїЄє'-]+$",
    message="Name can contain only letters, apostrophes and hyphens."
)

phone_validator = RegexValidator(
    regex=r"^\+380\d{9}$",
    message="Phone number must be in format +380XXXXXXXXX"
)


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
    first_name = models.CharField(max_length=255, validators=[name_validator])
    last_name = models.CharField(max_length=255, validators=[name_validator])
    birth_date = models.DateField()
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_validator]
    )
    diagnosis = models.TextField(max_length=255, default="-")

    class Meta:
        ordering = ["birth_date"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("clinic:patient-detail", kwargs={"pk": self.pk})


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
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_appointment"
            )
        ]

    def clean(self):
        if self.doctor and self.appointment_date:
            time_conflict = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date__gt=self.appointment_date - timedelta(minutes=10),
                appointment_date__lt=self.appointment_date + timedelta(minutes=10)
            ).exclude(pk=self.pk)

            if time_conflict.exists():
                raise ValidationError(
                    "This doctor already has an appointment within 10 minutes"
                )

    def __str__(self):
        return f"({self.appointment_date:%d.%m.%Y}) {self.patient}"


class CTScan(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="ct_scans"
    )
    image = models.ImageField(
        upload_to="ct_scan/"
    )
    scan_date = models.DateTimeField()
    description = models.TextField(max_length=255, blank=True, default="-")

    class Meta:
        ordering = ["-scan_date"]
        verbose_name = "CT Scan"
        verbose_name_plural = "CT Scans"

    def detail_image_preview(self):
        return mark_safe(
            f"<img src='{self.image.url}' "
            f"alt='' "
            f"width='{self.image.width}' "
            f"height='{self.image.height}'>"
        )

    def list_image_preview(self):
        return mark_safe(
            f"<img src='{self.image.url}' "
            f"alt='' "
            f"width='195' "
            f"height='160' "
        )

    def __str__(self):
        return f"CT Scan #{self.id} - {self.patient}"
