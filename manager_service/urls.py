from django.urls import path

from .views import index

app_name = 'manager_service'

urlpatterns = [
    path("", index, name="index"),
]

