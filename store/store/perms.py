from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOrderItemOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user


class IsOrderItemInCart(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.status == "CART"
