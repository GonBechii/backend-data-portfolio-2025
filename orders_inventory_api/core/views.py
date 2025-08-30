from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import Product, Customer, Order
from .serializers import (
    ProductSerializer,
    CustomerSerializer,
    OrderSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsReadOnly
from drf_spectacular.openapi import AutoSchema


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    # Público en lectura; si lo intentaran escribir, exige login
    permission_classes = [IsReadOnly]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ["sku", "name"]
    ordering_fields = ["id", "name", "price", "stock"]
    filterset_fields = {
        # ?sku=ALM-CAF-500 | ?sku__icontains=CAF
        "sku": ["exact", "icontains"],
        "price": ["gte", "lte"],        # ?price__gte=1000&price__lte=5000
        "stock": ["gte", "lte"],        # ?stock__gte=10
    }


class CustomerViewSet(viewsets.ModelViewSet):
    schema = AutoSchema()
    queryset = Customer.objects.all().order_by("id")
    serializer_class = CustomerSerializer
    # Requiere usuario autenticado para TODO
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ["name", "email"]
    ordering_fields = ["id", "name"]
    filterset_fields = {
        "name": ["icontains", "istartswith"],
        "email": ["icontains"],
        "id": ["exact"],
    }


class OrderViewSet(viewsets.ModelViewSet):
    queryset = (
        Order.objects
        .select_related("customer")
        .prefetch_related("items__product")
        .order_by("-id")
    )
    serializer_class = OrderSerializer
    # Requiere usuario autenticado para TODO
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ["customer__name", "status"]
    ordering_fields = ["id", "created_at", "total", "subtotal"]
    filterset_fields = {
        "status": ["exact"],          # ?status=PENDIENTE
        "customer": ["exact"],        # ?customer=1
        # si created_at es DateTimeField:
        # ?created_at__date__gte=2025-08-01
        "created_at": ["date", "date__gte", "date__lte"],
    }
