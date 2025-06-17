from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic

from .forms import WorkerSearchForm, WorkerCreationForm, TaskSearchForm, TaskForm
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
    template_name = "manager_service/profile.html"
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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 10

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_worker_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Worker.objects.all()
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    template_name = "manager_service/worker_detail.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 10
    template_name = "manager_service/task_list.html"

    def get_context_data(self, *, object_list = ..., **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_task_form"] = TaskSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "manager_service/task_form.html"


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "manager_service/task_form.html"


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "manager_service/task_detail.html"


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("manager_service:worker-list")

class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("manager_service:task-list")