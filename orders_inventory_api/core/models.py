from django.db import models

# Create your models here.


class Product(models.Model):
    sku = models.CharField(max_length=30,  unique=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"
