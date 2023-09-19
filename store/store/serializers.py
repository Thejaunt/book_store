from rest_framework import serializers

from .models import Book, Order, OrderItem


class WarehouseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    quantity = serializers.IntegerField()


class BookListSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source="get_absolute_url", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "price", "quantity", "url"]
        read_only_fields = ["__all__"]


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "price", "quantity", "id_warehouse"]
        read_only_fields = ["id", "title", "price", "quantity", "id_warehouse"]


class CartBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["url", "title", "price"]
        read_only_fields = ["url", "title", "price"]


class OrderItemSerializer(serializers.ModelSerializer):
    queryset = Book.objects.all()
    book = CartBookSerializer(queryset, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "book"]
        read_only_fields = ["id", "customer", "book"]

    def validate_quantity(self, value):
        max_qty = self.context["max_qty"]
        inst = self.context.get("inst")
        if max_qty == 0:
            raise serializers.ValidationError(f"id [{inst.book.id}], title: [{inst.book.title}] Item is out of stock")
        if value > max_qty:
            raise serializers.ValidationError(
                f"id [{inst.book.id}], title: [{inst.book.title}] only ({max_qty}) items in-stock"
            )
        return value

    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity")
        instance.quantity = quantity
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    queryset = Order.objects.all().prefetch_related("orderitem_set").select_related("customer")
    orderitem_set = OrderItemSerializer(queryset, many=True, required=True)

    class Meta:
        model = Order
        fields = [
            "orderitem_set",
            "delivery_address",
        ]
        read_only_fields = ["status", "customer"]

    def update(self, instance, validated_data):
        quantity = validated_data.get("quantity")
        instance.quantity = quantity
        instance.save()
        return instance


class MakeOrderSerializer(serializers.ModelSerializer):
    delivery_address = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Order
        fields = ["id", "orderitem_set", "delivery_address"]


class DeliverySerializer(serializers.Serializer):
    delivery_address = serializers.CharField(max_length=255, required=True)