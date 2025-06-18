from django.test import TestCase
from django import forms
from manager_service.forms import (
    WorkerSearchForm, WorkerForm, TaskSearchForm, TaskForm, TaskTypeForm, PositionForm
)
from manager_service.models import Worker, Task, TaskType, Position
from django.contrib.auth import get_user_model


class FormsTests(TestCase):
    def setUp(self):
        # Create necessary objects for foreign key relationships
        self.position = Position.objects.create(name="Developer")
        self.task_type = TaskType.objects.create(name="Bug Fix")
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass",
            position=self.position
        )
        self.task = Task.objects.create(
            name="Test Task",
            deadline="2023-12-31T23:59",
            priority="HIGH",
            task_type=self.task_type
        )
        self.task.assignees.add(self.user)

    def test_worker_form_validation(self):
        # Test valid data
        data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'position': self.position.id
        }
        form = WorkerForm(data=data)
        self.assertTrue(form.is_valid())

        # Test invalid data (passwords don't match)
        data['password2'] = 'differentpassword'
        form = WorkerForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    # TaskForm Tests
    def test_task_form_fields(self):
        form = TaskForm()
        expected_fields = [
            'name', 'description', 'deadline',
            'priority', 'task_type', 'assignees', 'is_completed'
        ]
        self.assertEqual(list(form.fields.keys()), expected_fields)

    # TaskTypeForm Tests
    def test_task_type_form_fields(self):
        form = TaskTypeForm()
        self.assertIn('name', form.fields)
        self.assertEqual(len(form.fields), 1)

    def test_task_type_form_save(self):
        data = {'name': 'New Task Type'}
        form = TaskTypeForm(data=data)
        self.assertTrue(form.is_valid())
        task_type = form.save()
        self.assertEqual(task_type.name, 'New Task Type')


    def test_position_form_save(self):
        data = {'name': 'New Position'}
        form = PositionForm(data=data)
        self.assertTrue(form.is_valid())
        position = form.save()
        self.assertEqual(position.name, 'New Position')

    def test_position_form_validation_unique(self):
        # Create existing position
        Position.objects.create(name="Existing Position")

        # Test duplicate name
        data = {'name': 'Existing Position'}
        form = PositionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
