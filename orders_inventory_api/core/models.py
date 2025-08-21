from django.db import models
from decimal import Decimal
from django.db.models import Sum

# Create your models here.


class Product(models.Model):
    sku = models.CharField(max_length=30,  unique=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class Customer(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["created_at"])
        ]

    def __str__(self):
        return f"{self.name} <{self.email}>"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PAID = "PAID", "Pagado"
        SHIPPED = "SHIPPED", "Enviado"
        CANCELLED = "CANCELLED", "Cancelado"

    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    # pequeña ayuda: esta funcion recalcula totales con lo que exista en Items
    def recompute_totals(self, *, save=True):
        subtotal = self.items.aggregate(s=Sum("line_total"))[
            "s"] or Decimal("0")
        self.subtotal = subtotal
        self.total = subtotal  # podemos agregar iva o descuentos
        if save:
            self.save(update_fields=["subtotal", "total"])
        return self.subtotal, self.total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    # ✅ permitir null y que el form no lo exija
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    # ✅ se calcula; no editable en el admin
    line_total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, editable=False)

    class Meta:
        unique_together = (("order", "product"),)
        constraints = [
            models.CheckConstraint(check=models.Q(
                quantity__gt=0), name="quantity_gt_0"),
        ]

    def save(self, *args, **kwargs):
        # si no viene el precio unitario, toma el del producto actual
        if self.unit_price:
            self.unit_price = self.product.price
        # Total de linea = precio * cantidad
        self.line_total = (self.unit_price or Decimal(0)) * \
            Decimal(self.quantity or 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} · {self.product.sku} x {self.quantity}"
