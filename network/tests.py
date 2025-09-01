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


    def test_factory_cannot_have_debt(self):
        """Завод не может иметь задолженность"""
        url = reverse("node-list")
        data = {
            "node_type": NetworkNode.FACTORY,
            "name": "Завод 3",
            "email": "f3@test.com",
            "country": "Россия",
            "city": "Тверь",
            "street": "Советская",
            "house_number": "5",
            "debt": "100.00",  # ошибка
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_supplier_cannot_be_self(self):
        """Нельзя быть своим же поставщиком"""
        url = reverse("node-detail", args=[self.factory.id])
        data = {
            "supplier": self.factory.id
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_can_create_ip_with_supplier(self):
        """ИП может иметь поставщика"""
        url = reverse("node-list")
        data = {
            "node_type": NetworkNode.ENTREPRENEUR,
            "name": "ИП Иванов",
            "email": "ip@test.com",
            "country": "Россия",
            "city": "Рязань",
            "street": "Молодежная",
            "house_number": "2",
            "supplier": self.factory.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #
    # class ProductAPITest(APITestCase):
    #     def setUp(self):
    #         self.user = User.objects.create_user(
    #             email="test2@test.com", password="12345", is_staff=True, is_active=True
    #         )
    #         self.client.force_authenticate(self.user)
    #
    #         self.factory = NetworkNode.objects.create(
    #             node_type=NetworkNode.FACTORY,
    #             name="Завод",
    #             email="factory@test.com",
    #             country="Россия",
    #             city="Москва",
    #             street="Ленина",
    #             house_number="1",
    #         )
    #
    #     def test_create_product(self):
    #         """Продукт создаётся нормально"""
    #         url = reverse("product-list")
    #         data = {
    #             "name": "Телевизор",
    #             "model": "LG123",
    #             "release_date": "2024-01-01",
    #             "supplier": self.factory.id,
    #         }
    #         response = self.client.post(url, data)
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

