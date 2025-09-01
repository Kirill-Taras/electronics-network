from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import NetworkNode, Product
from .permissions import IsActiveStaff
from .serializers import NetworkNodeSerializer, ProductSerializer


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD для звеньев сети.
    Только для активных пользователей.
    Фильтрация по стране.
    """

    queryset = (
        NetworkNode.objects.select_related("supplier")
        .prefetch_related("products")
        .all()
    )
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ("country",)  # фильтрация по стране
    search_fields = ("name", "email", "city")
    ordering_fields = ("created_at", "name")


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD для продуктов.
    Только для активных пользователей.
    Фильтрация по дате и поставщику.
    """

    queryset = Product.objects.select_related("supplier").all()
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = ("release_date", "supplier")
    search_fields = ("name", "model")
    ordering_fields = ("release_date", "name")
