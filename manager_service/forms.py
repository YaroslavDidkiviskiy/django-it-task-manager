from django import forms
from django.contrib.auth.forms import UserCreationForm

from manager_service.models import Worker, Task, Position, TaskType


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search worker by username"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class WorkerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "username",
            "first_name",
            "last_name",
            "position",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search a task by name"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "deadline", "priority", "task_type", "assignees", "is_completed")
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "is_completed": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class TaskTypeForm(forms.ModelForm):
    class Meta:
        model = TaskType
        fields = ("name",)


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ("name",)
