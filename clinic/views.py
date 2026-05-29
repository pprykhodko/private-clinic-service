from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from clinic.models import Doctor, Patient, Appointment, CTScan


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_doctors = Doctor.objects.count()
    num_patients = Patient.objects.count()
    num_appointments = Appointment.objects.count()
    num_images = CTScan.objects.count()
    context = {
        "num_doctors": num_doctors,
        "num_patients": num_patients,
        "num_appointments": num_appointments,
        "num_images": num_images,
    }
    return render(request, "clinic/index.html", context=context)


class DoctorListView(LoginRequiredMixin, generic.ListView):
    model = Doctor


class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
