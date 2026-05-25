from django.urls import path, include

from clinic.views import index


urlpatterns = [
    path("", index, name="index"),
]

app_name = "clinic"