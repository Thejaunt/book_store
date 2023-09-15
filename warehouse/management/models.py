from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    name = models.CharField(max_length=150, default="None")
    email = models.EmailField(unique=True)
    store_id = models.IntegerField()
    delivery_address = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}. {self.delivery_address}"


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    id_store = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    place = models.ForeignKey("BookPlace", on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.title


class BookPlace(models.Model):
    place = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.place


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f"{self.customer}, {self.book}, {self.quantity}"


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        ORDERED = "ORDERED", _("Ordered")
        SUCCESS = "SUCCESS", _("Success")
        FAILED = "FAILED", _("Failed")

    status = models.CharField(max_length=7, choices=OrderStatus.choices, default=OrderStatus.ORDERED)
    delivery_address = models.CharField(max_length=255)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.status
