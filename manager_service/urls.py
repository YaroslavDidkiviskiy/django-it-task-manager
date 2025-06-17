from django.urls import path
from . import views

app_name = 'manager_service'

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.ProfileDetailView.as_view(), name="profile-detail-view"),

    # Workers
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("workers/create/", views.WorkerCreateView.as_view(), name="worker-create"),
    path("workers/<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("workers/<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("workers/<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="worker-delete"),

    # Tasks
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),

    # Positions
    path("positions/", views.PositionListView.as_view(), name="position-list"),
    path("positions/create/", views.PositionCreateView.as_view(), name="position-create"),
    path("positions/<int:pk>/", views.PositionDetailView.as_view(), name="position-detail"),
    path("positions/<int:pk>/update/", views.PositionUpdateView.as_view(), name="position-update"),
    path("positions/<int:pk>/delete/", views.PositionDeleteView.as_view(), name="position-delete"),

    # Task Types
    path("task-types/", views.TaskTypeListView.as_view(), name="task-type-list"),
    path("task-types/<int:pk>/", views.TaskTypeDetailView.as_view(), name="task-type-detail"),
    path("task-types/create/", views.TaskTypeCreateView.as_view(), name="task-type-create"),
    path("task-types/<int:pk>/update/", views.TaskTypeUpdateView.as_view(), name="task-type-update"),
    path("task-types/<int:pk>/delete/", views.TaskTypeDeleteView.as_view(), name="task-type-delete"),
]
