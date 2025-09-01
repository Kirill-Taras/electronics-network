from rest_framework import serializers
from .models import NetworkNode, Product


class SupplierShortSerializer(serializers.ModelSerializer):
    """Краткая информация о поставщике (id, название, email)."""

    class Meta:
        model = NetworkNode
        fields = ("id", "name", "email")


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта."""

    class Meta:
        model = Product
        fields = ("id", "name", "model", "release_date", "supplier")
        read_only_fields = ("id",)


class NetworkNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор звена сети.
    - products: вложенный список продуктов (только чтение).
    - level: вычисляемое поле (глубина в иерархии).
    - debt: запрет изменения через API — делаем read_only.
    - supplier: вложенный список поставщиков.
    """

    products = ProductSerializer(many=True, read_only=True)
    supplier = serializers.PrimaryKeyRelatedField(
        queryset=NetworkNode.objects.all(),
        required=False,
        allow_null=True
    )
    supplier_info = SupplierShortSerializer(source='supplier', read_only=True)
    level = serializers.SerializerMethodField(read_only=True)
    debt = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "node_type",
            "name",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "supplier_info",
            "debt",
            "created_at",
            "level",
            "products",
        )
        read_only_fields = ("id", "node_type", "created_at", "level", "products", "debt")

    def validate_supplier(self, value):
        """
        Проверка:
        - у завода не может быть поставщика
        - Нельзя быть своим же поставщиком
        - Завод не может иметь задолженность
        """
        node_type = self.initial_data.get("node_type")
        debt = self.initial_data.get("debt")
        if node_type == NetworkNode.FACTORY and value is not None:
            raise serializers.ValidationError("У завода не может быть поставщика.")
        if node_type == NetworkNode.FACTORY and debt not in (None, 0, "0", "0.0"):
            raise serializers.ValidationError("У завода не может быть задолженности перед поставщиком.")
        if value and self.instance and value.pk == self.instance.pk:
            raise serializers.ValidationError("Поставщик не может быть самим собой.")
        return value


    def get_level(self, obj):
        """
        Вычисляем уровень в иерархии:
        - завод (supplier=None) -> 0
        - если supplier есть -> уровень родителя + 1
        """
        if not obj.supplier:
            return 0
        return obj.supplier.level + 1
