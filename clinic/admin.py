from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clinic.models import Doctor, Patient, Appointment, CTScan
from clinic.forms import CTScanForm


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("specialization",)
    fieldsets = UserAdmin.fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "specialization",
                        "hire_date",
                    )
                },
            ),
        )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "specialization",
                        "hire_date",
                    )
                },
            ),
        )
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "birth_date",
        "phone_number",
    )
    search_fields = ("first_name", "last_name")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "notes")


@admin.register(CTScan)
class CTScanAdmin(admin.ModelAdmin):
    form = CTScanForm
    readonly_fields = ("detail_image_preview",)
    list_display = ("__str__", "scan_date", "list_image_preview")
