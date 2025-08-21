from django.contrib import admin
from .models import Product, Customer, Order, OrderItem
from django import forms
# Register your models here.


class OrderItemInLineForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        product = cleaned.get("product")
        unit_price = cleaned.get("unit_price")
        qty = cleaned.get("quantity") or 0

        # ✅ si el precio no se escribe en el form, usar el del producto
        if product and unit_price in (None, ""):
            cleaned["unit_price"] = product.price

        if qty <= 0:
            self.add_error("quantity", "La cantidad debe ser mayor que 0.")
        return cleaned


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price', 'stock')
    search_fields = ('sku', 'name')
    list_per_page = 50


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page = 50


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemInLineForm       # usar el form pque rellena unit_price
    extra = 0
    fields = ("product", "quantity", "unit_price", "line_total")
    readonly_fields = ("line_total",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "status",
                    "subtotal", "total", "created_at")
    list_filter = ("status", "created_at")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]

    # Cuando guardas una orden con líneas, recalcula totales
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.recompute_totals()
