from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

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



class ProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "manager_service/profile_detail_view.html"
    context_object_name = "worker"

    def get_object(self, **kwargs):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()

        tasks = worker.assigned_tasks.all()
        context['total_tasks'] = tasks.count()
        context['completed_tasks'] = tasks.filter(is_completed=True).count()
        context['pending_tasks'] = context['total_tasks'] - context['completed_tasks']

        return context