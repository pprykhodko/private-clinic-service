from django.urls import path

from clinic.views import index, DoctorListView

urlpatterns = [
    path("", index, name="index"),
    path("doctors/", DoctorListView.as_view(), name="doctor-list"),
]

app_name = "clinic"
