from django.urls import path

from .views import BookListView, BookDetailView, CartView, OrderItemView

urlpatterns = [
    path("books/", BookListView.as_view()),
    path("book/<int:pk>", BookDetailView.as_view(), name="book-detail"),
    path("cart/", CartView.as_view({"get": "retrieve", "post": "create"}), name="cart"),
    path("order-item/<int:pk>", OrderItemView.as_view(), name="order-item"),
]
