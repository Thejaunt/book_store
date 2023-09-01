from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


Customer = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    id_warehouse = models.IntegerField()


class OrderItem(models.Model):
    quantity = models.IntegerField()

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CART = "CART", _("Cart")
        ORDERED = "ORDERED", _("Ordered")
        SUCCESS = "SUCCESS", _("Success")
        FAILED = "FAILED", _("Failed")

    status = models.CharField(max_length=7, choices=OrderStatus.choices, default=OrderStatus.CART)
    delivery_address = models.CharField(max_length=255)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["customer", "order_item"]



