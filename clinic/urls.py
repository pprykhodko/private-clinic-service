from django.urls import path

from clinic.views import (
    index,
    DoctorListView,
    PatientListView,
    PatientCreateView,
    PatientDetailView,
    PatientUpdateView,
    PatientDeleteView,
    AppointmentListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
    path("patients/", PatientListView.as_view(), name="patient-list"),
    path(
        "patients/create/",
        PatientCreateView.as_view(),
        name="patient-create"
    ),
    path(
        "patients/<int:pk>/",
        PatientDetailView.as_view(),
        name="patient-detail"
    ),
    path(
        "patients/<int:pk>/update/",
        PatientUpdateView.as_view(),
        name="patient-update"
    ),
    path(
        "patients/<int:pk>/delete/",
        PatientDeleteView.as_view(),
        name="patient-delete"
    ),
    path(
        "appointments/",
        AppointmentListView.as_view(),
        name="appointment-list"
    ),
]

app_name = "clinic"
