from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from network.models import NetworkNode

User = get_user_model()


class UserPermissionAPITest(APITestCase):
    def setUp(self):
        """
        Создаём три типа пользователей:
        1. Активный сотрудник (staff=True, is_active=True) — должен иметь доступ.
        2. Неактивный сотрудник (staff=True, is_active=False) — доступ запрещён.
        3. Обычный пользователь (staff=False, is_active=True) — доступ запрещён.
        """
        self.active_staff = User.objects.create_user(
            email="staff_active@test.com",
            password="12345",
            is_staff=True,
            is_active=True,
        )
        self.inactive_staff = User.objects.create_user(
            email="staff_inactive@test.com",
            password="12345",
            is_staff=True,
            is_active=False,
        )
        self.regular_user = User.objects.create_user(
            email="user@test.com", password="12345", is_staff=False, is_active=True
        )

        # Создаём объект сети для теста
        self.factory = NetworkNode.objects.create(
            node_type=NetworkNode.FACTORY,
            name="Завод",
            email="factory@test.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        # URL для проверки доступа к API
        self.url = reverse("node-list")

    def test_active_staff_has_access(self):
        """Активный сотрудник имеет доступ к API"""
        self.client.force_authenticate(self.active_staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactive_staff_denied(self):
        """Неактивный сотрудник получает 403 Forbidden"""
        self.client.force_authenticate(self.inactive_staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_denied(self):
        """Обычный пользователь получает 403 Forbidden"""
        self.client.force_authenticate(self.regular_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_denied(self):
        """Неавторизованный пользователь получает 401 Unauthorized"""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
