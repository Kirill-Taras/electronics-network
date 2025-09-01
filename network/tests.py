from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import NetworkNode, Product
from django.contrib.auth import get_user_model

User = get_user_model()


class NetworkNodeAPITest(APITestCase):
    def setUp(self):
        # создаём пользователя и логиним
        self.user = User.objects.create_user(
            email="test@test.com", password="12345", is_staff=True, is_active=True
        )
        self.client.force_authenticate(self.user)

        # базовый завод
        self.factory = NetworkNode.objects.create(
            node_type=NetworkNode.FACTORY,
            name="Завод",
            email="factory@test.com",
            country="Россия",
            city="Москва",
            street="Ленина",
            house_number="1",
        )

        # создаём розничную сеть с заводом как поставщиком
        self.retail = NetworkNode.objects.create(
            node_type=NetworkNode.RETAIL,
            name="Розница",
            email="retail@test.com",
            country="Россия",
            city="Москва",
            street="Тверская",
            house_number="10",
            supplier=self.factory
        )

        # создаём ИП с розницей как поставщиком
        self.entrepreneur = NetworkNode.objects.create(
            node_type=NetworkNode.ENTREPRENEUR,
            name="ИП Петров",
            email="ip2@test.com",
            country="Россия",
            city="Москва",
            street="Молодёжная",
            house_number="5",
            supplier=self.retail
        )

    def test_factory_cannot_have_supplier(self):
        """Завод не может иметь поставщика"""
        url = reverse("node-list")
        data = {
            "node_type": NetworkNode.FACTORY,
            "name": "Завод 2",
            "email": "f2@test.com",
            "country": "Россия",
            "city": "СПб",
            "street": "Пушкина",
            "house_number": "10",
            "supplier": self.factory.id,  # ошибка
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_levels_hierarchy(self):
        """Проверка уровней в иерархии: завод=0, розница=1, ИП=2"""
        self.assertEqual(self.factory.level, 0)
        self.assertEqual(self.retail.level, 1)
        self.assertEqual(self.entrepreneur.level, 2)

