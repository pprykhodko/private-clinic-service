from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clinic.models import Doctor, Patient, Appointment, CTScan


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("specialization", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("specialization", "years_of_experience", )}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("specialization", "years_of_experience",)}),)
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date", "phone_number", )
    search_fields = ("first_name", "last_name")

    @admin.display(description="Patient")
    def full_name(self, obj):
        return str(obj)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "notes")


@admin.register(CTScan)
class CTScanAdmin(admin.ModelAdmin):
    pass
