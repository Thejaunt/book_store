from django.db import transaction
from rest_framework import generics, viewsets, status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from .models import Book, Order, OrderItem
from .perms import ReadOnly, IsOrderItemOwnerPermission, IsOrderItemInCart
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    OrderSerializer,
    OrderItemSerializer,
    MakeOrderSerializer,
)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class BookDetailView(generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer

    def create(self, request, *args, **kwargs):
        """Adding a book into the Cart"""
        obj = self.get_object()
        order_instance, created = Order.objects.get_or_create(customer=request.user, status="CART")

        order_items = [oi for oi in order_instance.orderitem_set.all()]
        # if the book is already in the cart - increment the cart quantity
        for order_item in order_items:
            if order_item.book == obj:
                if order_item.quantity < obj.quantity:
                    order_item.quantity += 1
                    order_item.save()
                return Response({"message": "book has been added to the cart"}, status=status.HTTP_200_OK)
        if obj.quantity > 0:
            OrderItem.objects.create(
                book=obj,
                order=order_instance,
                customer=request.user,
                quantity=1,
            )
        else:
            return Response(data={f"{obj.title} is out of stock. Can't add it into the CART"})
        return Response({"message": "book has been added to the cart"}, status=status.HTTP_201_CREATED)


class CartView(viewsets.ModelViewSet):
    queryset = Order.objects.filter(status="CART")
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return MakeOrderSerializer
        return self.serializer_class

    def retrieve(self, request, *args, **kwargs):
        instance, created = Order.objects.get_or_create(customer=request.user, status="CART")
        serializer = OrderSerializer(instance, context={"request": request})
        data = serializer.data
        data["total_price"] = instance.total_price()
        return Response(data)

    def create(self, request, *args, **kwargs):
        try:
            instance = Order.objects.prefetch_related("orderitem_set", "orderitem_set__book").get(
                customer=request.user, status="CART"
            )
            items = instance.orderitem_set.all()
            if items.count() < 1:
                return Response("cart is empty")
        except Order.DoesNotExist:
            return Response("CART is empty")

        with transaction.atomic():
            books = []
            for item in items:
                ser = OrderItemSerializer(
                    data={"quantity": item.quantity, "id": item.id},
                    context={"request": request, "max_qty": item.book.quantity, "inst": item},
                )
                ser.is_valid(raise_exception=True)
                book = item.book
                book.quantity -= item.quantity
                books.append(book)
            Book.objects.bulk_update(books, ["quantity"])
            instance.status = "ORDERED"
            instance.save()
            #  SEND INSTANCE TO OTHER SERVICE

        return Response("serializer.data")


class OrderItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all().select_related("order", "book")
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOrderItemOwnerPermission, IsOrderItemInCart]
    serializer_class = OrderItemSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        max_qty = instance.book.quantity
        serializer = OrderItemSerializer(
            instance,
            data=request.data,
            context={"request": request, "max_qty": max_qty, "inst": instance},
            partial=partial,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
