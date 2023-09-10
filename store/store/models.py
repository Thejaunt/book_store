from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


Customer = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    id_warehouse = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("book-detail", kwargs={"pk": self.pk})


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return f"ITEM: {self.book.title}, CUSTOMER: {self.customer}, STATUS: {self.order.status} "

    def total_price(self):
        total = self.book.price * self.quantity
        return round(float(total), 2)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        CART = "CART", _("Cart")
        ORDERED = "ORDERED", _("Ordered")
        SUCCESS = "SUCCESS", _("Success")
        FAILED = "FAILED", _("Failed")

    status = models.CharField(max_length=7, choices=OrderStatus.choices, default=OrderStatus.CART)
    delivery_address = models.CharField(max_length=255)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "status"],
                name="unique_cart_per_customer",
                condition=Q(status="CART"),
            )
        ]

    def total_price(self):
        total = float()
        for item in self.orderitem_set.all():
            total += item.total_price()
        return round(float(total), 2)
