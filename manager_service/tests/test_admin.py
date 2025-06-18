from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from manager_service.models import Position  # Import Position model


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()


        self.position = Position.objects.create(name="Developer")

        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
            position=self.position,
        )
        self.client.force_login(self.admin_user)


        self.worker = get_user_model().objects.create_user(
            username="worker",
            password="testworker",
            position=self.position,
        )

    def test_worker_position_listed_in_changelist(self):
        """Test that worker's position appears in admin list view"""
        url = reverse("admin:manager_service_worker_changelist")
        res = self.client.get(url)

        # Check for position name
        self.assertContains(res, self.worker.position.name)

    def test_worker_position_listed_in_detail(self):
        """Test that worker's position appears in admin detail view"""
        url = reverse(
            "admin:manager_service_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)

        self.assertContains(res, self.worker.position.name)
