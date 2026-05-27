from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from clinic.models import Doctor, Patient, Appointment, CTScan


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("specialization", )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info",
          {
              "fields":
                  (
                      "specialization",
                      "years_of_experience",
                  )
          }
          ),
         )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info",
          {
              "fields":
                  (
                      "first_name",
                      "last_name",
                      "specialization",
                      "years_of_experience",
                  )
          }
          ),
         )
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("__str__", "birth_date", "phone_number", )
    search_fields = ("first_name", "last_name")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "notes")


@admin.register(CTScan)
class CTScanAdmin(admin.ModelAdmin):
    readonly_fields = ("detail_image_preview",)
    list_display = ("__str__", "scan_date", "list_image_preview")
