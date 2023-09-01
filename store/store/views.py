import jwt
from rest_framework import generics
from rest_framework import permissions

from .models import Book
from .serializers import BookListSerializer, BookDetailSerializer
from core import settings


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.auth)
        return request.method in permissions.SAFE_METHODS


class IsAdminUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        print(request.COOKIES.get("jwt"))
        print(jwt.decode(request.COOKIES.get("jwt"), settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT.get("ALGORITHM")))
        return bool(request.user and request.user.is_staff)


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer



