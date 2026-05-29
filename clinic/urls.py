from django.urls import path

from clinic.views import index, DoctorListView, PatientListView

urlpatterns = [
    path("", index, name="index"),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("patients/", PatientListView.as_view(), name="patient-list"),
]

app_name = "clinic"
