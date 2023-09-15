from django.contrib import admin

from .models import Book, BookPlace, Customer, Order, OrderItem


admin.site.register(Book)
admin.site.register(BookPlace)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
