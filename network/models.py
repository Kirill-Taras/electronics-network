from django.db import models
from decimal import Decimal


class NetworkNode(models.Model):
    """
    Модель звена сети (завод / розничная сеть / индивидуальный предприниматель).
    Каждое звено может иметь поставщика (родительский элемент) и собственные продукты.
    """

    name = models.CharField(max_length=255, verbose_name="Название")
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clients",
        verbose_name="Поставщик",
        help_text="Предыдущее звено в иерархии сети"
    )

    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Задолженность перед поставщиком"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    class Meta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self):
        return f"{self.name} ({self.city})"


class Product(models.Model):
    """
    Модель продукта, привязанного к определенному звену сети.
    """

    name = models.CharField(max_length=255, verbose_name="Название продукта")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    supplier = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Поставщик"
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"
