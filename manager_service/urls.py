from django.urls import path

from .views import (index,
                    ProfileDetailView,
                    WorkerListView,
                    WorkerCreateView,
                    WorkerDetailView,
                    TaskListView,
                    TaskCreateView,
                    TaskUpdateView,
                    TaskDetailView,
                    TaskDeleteView,
                    WorkerDeleteView,
                    PositionListView,
                    TaskTypeListView)

app_name = 'manager_service'

urlpatterns = [
    path("", index, name="index"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail-view"),
    path("workers/", WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/delete", WorkerDeleteView.as_view(), name="worker-delete"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("positions/", PositionListView.as_view(), name="position-list"),

    path("task-types/", TaskTypeListView.as_view(), name="task-type-list"),
]

