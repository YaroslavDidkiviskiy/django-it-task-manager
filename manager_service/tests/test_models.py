from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from manager_service.models import Position, TaskType, Worker, Task
from django.contrib.auth import get_user_model


class PositionModelTest(TestCase):
    def test_position_creation(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(str(position), "Developer")
        self.assertEqual(position.name, "Developer")
        self.assertEqual(Position._meta.ordering, ('name',))

    def test_position_unique_name(self):
        Position.objects.create(name="Designer")
        with self.assertRaises(Exception):
            Position.objects.create(name="Designer")

    def test_get_absolute_url(self):
        position = Position.objects.create(name="Manager")
        expected_url = reverse("manager_service:position-detail", kwargs={"pk": position.pk})
        self.assertEqual(position.get_absolute_url(), expected_url)


class TaskTypeModelTest(TestCase):
    def test_task_type_creation(self):
        task_type = TaskType.objects.create(name="Bug Fix")
        self.assertEqual(str(task_type), "Bug Fix")
        self.assertEqual(task_type.name, "Bug Fix")
        self.assertEqual(TaskType._meta.ordering, ('name',))

    def test_get_absolute_url(self):
        task_type = TaskType.objects.create(name="Feature")
        expected_url = reverse("manager_service:task-type-detail", kwargs={"pk": task_type.pk})
        self.assertEqual(task_type.get_absolute_url(), expected_url)


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

    def test_worker_creation(self):
        worker = Worker.objects.create_user(
            username="john_doe",
            password="testpass",
            position=self.position
        )
        self.assertEqual(str(worker), "john_doe - Developer")
        self.assertEqual(worker.username, "john_doe")
        self.assertEqual(worker.position, self.position)


    def test_get_absolute_url(self):
        worker = Worker.objects.create_user(username="testuser", password="testpass")
        expected_url = reverse("manager_service:worker-detail", kwargs={"pk": worker.pk})
        self.assertEqual(worker.get_absolute_url(), expected_url)


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.task_type = TaskType.objects.create(name="Testing")
        self.user1 = Worker.objects.create_user(username="user1", password="pass1", position=self.position)
        self.user2 = Worker.objects.create_user(username="user2", password="pass2", position=self.position)

        future_date = timezone.now() + timezone.timedelta(days=7)
        self.task = Task.objects.create(
            name="Test Task",
            description="Important task",
            deadline=future_date,
            priority="HIGH",
            task_type=self.task_type,
            is_completed=False
        )
        self.task.assignees.add(self.user1, self.user2)

    def test_task_creation(self):
        self.assertEqual(self.task.name, "Test Task")
        self.assertEqual(self.task.description, "Important task")
        self.assertEqual(self.task.priority, "HIGH")
        self.assertEqual(self.task.task_type, self.task_type)
        self.assertEqual(self.task.is_completed, False)
        self.assertEqual(list(self.task.assignees.all()), [self.user1, self.user2])

    def test_task_string_representation(self):
        expected_str = (
            f"Task: Test Task - High [Testing] до {self.task.deadline}. "
            f"\nAssignees: user1, user2 ❌"
        )
        self.assertEqual(str(self.task), expected_str)

    def test_get_absolute_url(self):
        expected_url = reverse("manager_service:task-detail", kwargs={"pk": self.task.pk})
        self.assertEqual(self.task.get_absolute_url(), expected_url)
