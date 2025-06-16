from django.urls import path

from .views import index, ProfileDetailView

app_name = 'manager_service'

urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail-view"),
]

