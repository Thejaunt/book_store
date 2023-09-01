from rest_framework import generics
from rest_framework import permissions

from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAdminUser | ReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
