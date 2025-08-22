from decimal import Decimal
from django.db import transaction
from django.db.models import F
from rest_framework import serializers

from .models import Product, Customer, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "sku", "name", "price", "stock")


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


# ---- Items: Escritura (Post) ----
class OrderItemWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "unit_price")

        def validate_quantity(self, value):
            if value <= 0:
                raise serializers.ValidationError(
                    "La cantidad debe ser mayor que 0.")
            return value

# ---- Items: Lectura (Get) ----


class OrderItemReadSerializers(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "unit_price", "line_total")


class OrderSerializer(serializers.ModelSerializer):
    # Entrada para crear: lista de items
    items = OrderItemWriteSerializer(many=True, write_only=True)
    # salida (detalle de items)
    items_detail = serializers.SerializerMethodField(read_only=True)
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all())

    class Meta:
        model = Order
        fields = (
            "id",
            "customer",
            "status",
            "subtotal",
            "total",
            "created_at",
            "items",                # write-only
            "items_detail"          # read-only
        )
        read_only_fields = ("subtotal", "total", "created_at")

    def get_items_detail(self, obj):
        # Funciona tangas o no related_name="items" en OrderItem.order
        related = getattr(obj, "items", None) or getattr(obj, "orderitem_set")
        return OrderItemReadSerializers(related.all(), many=True).data

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])

        if not items_data:
            raise serializers.ValidationError(
                {"items ": "Debe incluir al menos in ítem"})

        with transaction.atomic():
            order = Order.objects.create(**validated_data)

            # Bloqueamos los productos para descontar stock de forma segura
            product_ids = [item["product"].id for item in items_data]
            products = Product.objects.select_for_update().in_bulk(product_ids)

            subtotal = Decimal("0")

            for item in items_data:
                product = products[item["product"].id]
                qty = item["quantity"]
                unit_price = item.get("unit_price") or product.price

                # Validacion de Stock

                if product.stock < qty:
                    raise serializers.ValidationError(
                        f"Stock insuficiente para {product.sku} (disponible: {product.stock})"
                    )

                line_total = (unit_price * qty).quantize(Decimal("0.01"))

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    unit_price=unit_price,
                    line_total=line_total,
                )

                Product.objects.filter(pk=product.pk).update(
                    stock=F("stock") - qty)
                subtotal += line_total

            # Sin IVA por el momento
            order.subtotal = subtotal
            order.total = subtotal
            order.save(update_fields=["subtotal", "total"])

            return order
