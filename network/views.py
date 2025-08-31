from rest_framework import viewsets, filters
from .models import NetworkNode, Product
from .serializers import NetworkNodeSerializer, ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend


class NetworkNodeViewSet(viewsets.ModelViewSet):
    """
    CRUD для звеньев сети.
    Пока без строгих прав — AllowAny (можно заменить на IsAuthenticated позже).
    Фильтрация по стране.
    """
    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products").all()
    serializer_class = NetworkNodeSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("country",)  # фильтрация по стране
    search_fields = ("name", "email", "city")
    ordering_fields = ("created_at", "name")


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD для продуктов.
    """
    queryset = Product.objects.select_related("supplier").all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ("release_date", "supplier")
    search_fields = ("name", "model")
    ordering_fields = ("release_date", "name")
