from rest_framework.permissions import BasePermission

class IsValuer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) in ["valuer", "admin"]

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) in ["customer", "admin"]
