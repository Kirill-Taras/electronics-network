from django.contrib import admin

from .models import NetworkNode, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    """Обнуляем поле debt для выбранных объектов."""
    updated = queryset.update(debt=0)
    modeladmin.message_user(request, f"Задолженность обнулена у {updated} объектов.")


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "node_type",
        "level",
        "name",
        "city",
        "email",
        "supplier",
        "debt",
        "created_at",
    )
    list_filter = ("country", "city", "supplier")
    search_fields = ("name", "email", "city")
    ordering = ("-created_at",)
    verbose_name = "Сеть"
    actions = [clear_debt]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "release_date", "supplier")
    list_filter = ("release_date", "supplier")
    search_fields = ("name", "model")
    ordering = ("-release_date",)
    verbose_name = "Продукт"
