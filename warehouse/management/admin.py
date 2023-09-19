from django.contrib import admin
from django.shortcuts import get_object_or_404

from .models import Book, BookPlace, Customer, Order, OrderItem


@admin.action(description="In Progress Order")
def in_progress_order(modeladmin, request, queryset):
    for order in queryset:
        if order.status == "SUCCESS":
            books = []
            for order_item in order.orderitem_set.all():
                book = get_object_or_404(Book, pk=order_item.book.id)
                book.quantity += order_item.quantity
                books.append(book)
            Book.objects.bulk_update(books, ["quantity"])
    queryset.update(status="ORDERED")


@admin.action(description="Confirm Order")
def confirm_order(modeladmin, request, queryset):
    for order in queryset:
        if order.status == "SUCCESS":
            continue
        books = []
        for order_item in order.orderitem_set.all():
            book = Book.objects.get(id=order_item.book.id)
            if order_item.quantity > book.quantity:
                return None
            book.quantity -= order_item.quantity
            books.append(book)
        Book.objects.bulk_update(books, ["quantity"])
    queryset.update(status="SUCCESS")


@admin.action(description="Reject Order")
def reject_order(modeladmin, request, queryset):
    for order in queryset:
        if order.status == "SUCCESS":
            books = []
            for order_item in order.orderitem_set.all():
                book = get_object_or_404(Book, pk=order_item.book.id)
                book.quantity += order_item.quantity
                books.append(book)
            Book.objects.bulk_update(books, ["quantity"])
    queryset.update(status="FAILED")


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    fields = ["customer", "status", "delivery_address"]
    list_display = ["status", "customer", "delivery_address", "get_orderitems", "total_price"]
    list_select_related = ["customer"]
    inlines = [OrderItemInline]

    actions = [confirm_order, reject_order, in_progress_order]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("orderitem_set", "orderitem_set__book")

    @staticmethod
    def get_orderitems(obj):
        items = []
        for i in obj.orderitem_set.all():
            items.append(f"title: {i.book}, qty: {i.quantity}, place: {i.book.place}, price: {i.total_price()}")
        return " | ".join(items)


admin.site.register(Book)
admin.site.register(BookPlace)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
