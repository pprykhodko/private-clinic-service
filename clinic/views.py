from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from clinic.forms import (
    DoctorSearchForm,
    PatientForm,
    PatientSearchForm,
    AppointmentForm,
    AppointmentUpdateForm,
    AppointmentSearchForm,
    CTScanForm,
    CTScanSearchForm,
)
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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(DoctorListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = DoctorSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        doctor = self.request.GET.get("doctor")
        if doctor:
            return Doctor.objects.filter(
                Q(first_name__iregex=doctor.capitalize())
                | Q(last_name__iregex=doctor.capitalize())
            )
        return Doctor.objects.all()


class DoctorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context = super(DoctorDetailView, self).get_context_data(**kwargs)
        context["patient_list"] = self.object.patients.all().distinct()
        return context


class PatientListView(LoginRequiredMixin, generic.ListView):
    model = Patient
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)
        last_name = self.request.GET.get("last_name", "")
        context["search_form"] = PatientSearchForm(
            initial={"last_name": last_name}
        )
        return context

    def get_queryset(self):
        patient = self.request.GET.get("patient")
        if patient:
            return Patient.objects.filter(
                Q(first_name__iregex=patient.capitalize())
                | Q(last_name__iregex=patient.capitalize())
            )
        return Patient.objects.all()


class PatientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("clinic:patient-list")


class PatientDetailView(LoginRequiredMixin, generic.DetailView):
    model = Patient


class PatientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Patient
    form_class = PatientForm
    success_url = reverse_lazy("clinic:patient-list")


class PatientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Patient
    success_url = reverse_lazy("clinic:patient-list")


class AppointmentListView(LoginRequiredMixin, generic.ListView):
    model = Appointment
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(AppointmentListView, self).get_context_data(**kwargs)
        patient = self.request.GET.get("patient", "")
        context["search_form"] = AppointmentSearchForm(
            initial={
                "patient": patient
            }
        )
        return context

    def get_queryset(self):
        patient = self.request.GET.get("patient")
        if patient:
            return Appointment.objects.filter(
                Q(patient__first_name__iregex=patient.capitalize())
                | Q(patient__last_name__iregex=patient.capitalize())
            )
        return Appointment.objects.all()


class AppointmentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy("clinic:appointment-list")


class AppointmentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Appointment


class AppointmentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Appointment
    form_class = AppointmentUpdateForm
    success_url = reverse_lazy("clinic:appointment-list")


class AppointmentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Appointment
    success_url = reverse_lazy("clinic:appointment-list")


class CTScanListView(LoginRequiredMixin, generic.ListView):
    model = CTScan
    template_name = "clinic/ct_scan_list.html"
    context_object_name = "ct_scan_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CTScanListView, self).get_context_data(**kwargs)
        patient = self.request.GET.get("patient", "")
        context["search_form"] = CTScanSearchForm(initial={"patient": patient})
        return context

    def get_queryset(self):
        patient = self.request.GET.get("patient")
        if patient:
            return CTScan.objects.filter(
                Q(patient__first_name__iregex=patient.capitalize())
                | Q(patient__last_name__iregex=patient.capitalize())
            )
        return CTScan.objects.all()


class CTScanCreateView(LoginRequiredMixin, generic.CreateView):
    model = CTScan
    template_name = "clinic/ct_scan_form.html"
    form_class = CTScanForm
    success_url = reverse_lazy("clinic:ct-scan-list")


class CTScanDetailView(LoginRequiredMixin, generic.DetailView):
    model = CTScan
    template_name = "clinic/ct_scan_detail.html"


class CTScanDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = CTScan
    template_name = "clinic/ct_scan_confirm_delete.html"
    success_url = reverse_lazy("clinic:ct-scan-list")
