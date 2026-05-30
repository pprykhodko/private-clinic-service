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
    AppointmentCreateView,
    AppointmentDetailView,
    AppointmentUpdateView,
    AppointmentDeleteView,
    CTScanListView, CTScanCreateView,
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
    path(
        "appointments/create/",
        AppointmentCreateView.as_view(),
        name="appointment-create"
    ),
    path(
        "appointments/<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail"
    ),
    path(
        "appointments/<int:pk>/update/",
        AppointmentUpdateView.as_view(),
        name="appointment-update"
    ),
    path(
        "appointments/<int:pk>/delete/",
        AppointmentDeleteView.as_view(),
        name="appointment-delete"
    ),
    path(
        "ct-scans/",
        CTScanListView.as_view(),
        name="ct-scan-list"
    ),
    path(
        "ct-scans/create/",
        CTScanCreateView.as_view(),
        name="ct-scan-create"
    )
]

app_name = "clinic"
