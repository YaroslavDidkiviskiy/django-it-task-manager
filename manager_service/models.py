from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


PRIORITY_CHOICES = [
    ("URGENT", "Urgent"),
    ("HIGH", "High"),
    ("MEDIUM", "Medium"),
    ("LOW", "Low"),
]



class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager_service:position-detail", kwargs={"pk": self.pk})

class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("manager_service:task-type-detail", kwargs={"pk": self.pk})


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        if self.position:
            return f"{self.username} - {self.position.name}"
        return f"{self.username} - No Position"

    def get_absolute_url(self):
        return reverse("manager_service:worker-detail", kwargs={"pk": self.pk})

class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(
        validators=[MinValueValidator(now)]
    )
    is_completed =models.BooleanField(default=False)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10, default="MEDIUM", )
    task_type = models.ForeignKey(TaskType, on_delete=models.SET_NULL, null=True)
    assignees = models.ManyToManyField(Worker, related_name="assigned_tasks")

    def assignees_list(self):
        return ", ".join(worker.username for worker in self.assignees.all())
    assignees_list.short_description = 'Assignees'

    def __str__(self):
        task_type_name = self.task_type.name if self.task_type else "No Type"
        assignees = ", ".join(worker.username for worker in self.assignees.all())
        status = "✅" if self.is_completed else "❌"
        return f"Task: {self.name} - {self.get_priority_display()} [{task_type_name}] до {self.deadline}. \nAssignees: {assignees} {status}"

    def get_absolute_url(self):
        return reverse("manager_service:task-detail", kwargs={"pk": self.pk})
