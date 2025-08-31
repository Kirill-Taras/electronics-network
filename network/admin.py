from django.contrib import admin
from .models import NetworkNode, Product


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ("id", "node_type", "name", "city", "email", "supplier", "debt", "created_at")
    list_filter = ("country", "city", "supplier")
    search_fields = ("name", "email", "city")
    ordering = ("-created_at",)
    verbose_name = ("Сеть")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "release_date", "supplier")
    list_filter = ("release_date", "supplier")
    search_fields = ("name", "model")
    ordering = ("-release_date",)
    verbose_name = ("Продукт")
