from django.contrib import admin
from .models import Product
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'price', 'stock')
    search_fields = ('sku', 'name')
