from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import Product, Customer, Order
from .serializers import (
    ProductSerializer,
    CustomerSerializer,
    OrderSerializer,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsRead_only


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("id")
    serializer_class = ProductSerializer
    # Público en lectura; si lo intentaran escribir, exige login
    permission_classes = [IsRead_only]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ["sku", "name"]
    ordering_fields = ["name", "price", "stock"]
    filterset_fields = ["sku", "price", "stock"]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by("id")
    serializer_class = CustomerSerializer
    # Requiere usuario autenticado para TODO
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "id"]
    filterset_fields = ["name", "email"]


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
    filterset_fields = ["status", "customer"]
