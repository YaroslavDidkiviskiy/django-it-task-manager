from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Worker, Task, TaskType, Position


@login_required
def index(request):
    num_workers = Worker.objects.count()
    num_tasks = Task.objects.count()
    task_list = Task.objects.all()
    completed_tasks = Task.objects.filter(is_completed=True).count()

    context = {
        'num_workers': num_workers,
        'num_tasks': num_tasks,
        'task_list': task_list,
        'completed_tasks': completed_tasks,
    }

    return render(request, "manager_service/index.html", context=context)
