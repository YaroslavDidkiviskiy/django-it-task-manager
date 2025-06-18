from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from manager_service.models import Task, Worker, Position, TaskType

User = get_user_model()


class ViewTests(TestCase):
    def setUp(self):
        # Create test users
        self.position = Position.objects.create(name="Developer")
        self.admin = User.objects.create_superuser(
            username="admin",
            password="adminpass",
            position=self.position
        )
        self.worker = User.objects.create_user(
            username="worker",
            password="workerpass",
            position=self.position
        )

        # Create test task type
        self.task_type = TaskType.objects.create(name="Bug Fix")

        # Create test task
        self.task = Task.objects.create(
            name="Test Task",
            deadline=timezone.now() + timezone.timedelta(days=7),
            priority="HIGH",
            task_type=self.task_type,
        )
        self.task.assignees.add(self.worker)

        # Set up client
        self.client = Client()

    # Helper methods
    def login_admin(self):
        self.client.login(username="admin", password="adminpass")

    def login_worker(self):
        self.client.login(username="worker", password="workerpass")

    # Index View Tests
    def test_index_view(self):
        # Add login before accessing the protected view
        self.login_admin()

        response = self.client.get(reverse("manager_service:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/index.html")
        self.assertContains(response, "Task Manager")
        self.assertEqual(response.context["num_workers"], 2)
        self.assertEqual(response.context["num_tasks"], 1)

    def test_worker_create_view(self):
        self.login_admin()
        response = self.client.post(reverse("manager_service:worker-create"), {
            "username": "newuser",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "position": self.position.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_worker_detail_view(self):
        self.login_admin()
        url = reverse("manager_service:worker-detail", kwargs={"pk": self.worker.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/worker_detail.html")
        self.assertEqual(response.context["worker"], self.worker)

    def test_worker_delete_view(self):
        self.login_admin()
        url = reverse("manager_service:worker-delete", kwargs={"pk": self.worker.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username="worker").exists())

    def test_task_create_view(self):
        self.login_admin()
        response = self.client.post(reverse("manager_service:task-create"), {
            "name": "New Task",
            "deadline": timezone.now() + timezone.timedelta(days=3),
            "priority": "MEDIUM",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id]
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New Task").exists())

    def test_task_detail_view(self):
        self.login_admin()
        url = reverse("manager_service:task-detail", kwargs={"pk": self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/task_detail.html")
        self.assertEqual(response.context["task"], self.task)

    def test_task_update_view(self):
        self.login_admin()
        url = reverse("manager_service:task-update", kwargs={"pk": self.task.pk})
        response = self.client.post(url, {
            "name": "Updated Task",
            "deadline": self.task.deadline,
            "priority": "URGENT",
            "task_type": self.task_type.id,
            "assignees": [self.worker.id],
            "is_completed": True
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")
        self.assertTrue(self.task.is_completed)

    def test_task_delete_view(self):
        self.login_admin()
        url = reverse("manager_service:task-delete", kwargs={"pk": self.task.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name="Test Task").exists())

    # Position Views Tests
    def test_position_list_view(self):
        self.login_admin()
        response = self.client.get(reverse("manager_service:position-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/position-list.html")
        self.assertEqual(len(response.context["position_list"]), 1)

    def test_position_detail_view(self):
        self.login_admin()
        url = reverse("manager_service:position-detail", kwargs={"pk": self.position.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/position_detail.html")
        self.assertEqual(len(response.context["workers"]), 2)

    def test_position_create_view(self):
        self.login_admin()
        response = self.client.post(reverse("manager_service:position-create"), {
            "name": "Designer"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Position.objects.filter(name="Designer").exists())

    def test_position_update_view(self):
        self.login_admin()
        url = reverse("manager_service:position-update", kwargs={"pk": self.position.pk})
        response = self.client.post(url, {"name": "Senior Developer"})
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Senior Developer")

    def test_position_delete_view(self):
        self.login_admin()
        url = reverse("manager_service:position-delete", kwargs={"pk": self.position.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Position.objects.filter(name="Developer").exists())

    # TaskType Views Tests
    def test_tasktype_list_view(self):
        self.login_admin()
        response = self.client.get(reverse("manager_service:task-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/task_type_list.html")
        self.assertEqual(len(response.context["tasktype_list"]), 1)

    def test_tasktype_detail_view(self):
        self.login_admin()
        url = reverse("manager_service:task-type-detail", kwargs={"pk": self.task_type.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "manager_service/task_type_detail.html")

    def test_tasktype_create_view(self):
        self.login_admin()
        response = self.client.post(reverse("manager_service:task-type-create"), {
            "name": "Feature"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Feature").exists())

    def test_tasktype_update_view(self):
        self.login_admin()
        url = reverse("manager_service:task-type-update", kwargs={"pk": self.task_type.pk})
        response = self.client.post(url, {"name": "Bug Report"})
        self.assertEqual(response.status_code, 302)
        self.task_type.refresh_from_db()
        self.assertEqual(self.task_type.name, "Bug Report")
