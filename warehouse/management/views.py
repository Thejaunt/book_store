import json

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book, Customer, Order, OrderItem
from .serializers import BookSerializer


@api_view(("GET", "POST"))
def new_order_view(request):
    req = json.loads(request.body)
    customer_email = req.get("customer_email")
    delivery_address = req.get("order_delivery_address")
    order_items = req.get("order_items")
    with transaction.atomic():
        customer, created_c = Customer.objects.get_or_create(email=customer_email)
        order = Order.objects.create(customer=customer, delivery_address=delivery_address)
        for order_item in order_items:
            try:
                book = Book.objects.get(id=order_item.get("book_warehouse_id"))
            except Book.DoesNotExist:
                # maybe send email?
                return Response(data={"new order": "failed"}, status=status.HTTP_409_CONFLICT)

            OrderItem.objects.create(customer=customer, order=order, book=book, quantity=order_item.get("qty"))

    return Response(data={"new order": "done"}, status=status.HTTP_201_CREATED)


@api_view(("GET",))
def db_update(request):
    books = Book.objects.all()
    data = BookSerializer(books, many=True)
    return Response(data={"data": data.data}, status=status.HTTP_201_CREATED)