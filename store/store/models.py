from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(get_user_model()):
    pass


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    id_warehouse = models.IntegerField()


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CART = "CART", _("Cart")
        ORDERED = "ORDERED", _("Ordered")
        SUCCESS = "SUCCESS", _("Success")
        FAILED = "FAILED", _("Failed")

    user_id = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    status = models.CharField(max_length=7, choices=OrderStatus.choices, default=OrderStatus.CART)
    delivery_address = models.CharField(max_length=255)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
