from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Worker, Task, TaskType, Position

admin.site.register(Position)
admin.site.register(TaskType)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "name", "description",
        "deadline", "is_completed",
        "priority", "task_type",
        "assignees_list",
        ]
    list_filter = ["is_completed", "priority", "task_type"]
    date_hierarchy = "deadline"
    ordering = ["-deadline"]


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        ("Personal info", {"fields": ("first_name", "last_name", "position")}),
    )
