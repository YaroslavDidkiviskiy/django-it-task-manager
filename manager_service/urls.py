from django.urls import path

from .views import index, ProfileDetailView, WorkerListView, WorkerCreateView, WorkerDetailView

app_name = 'manager_service'

urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
]

