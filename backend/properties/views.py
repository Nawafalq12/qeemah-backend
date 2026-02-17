from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Property
from .serializers import PropertySerializer


def is_valuer(user):
    return getattr(user, "role", "") == "valuer"


def is_customer(user):
    return getattr(user, "role", "") == "customer"


class PropertyCreateView(generics.CreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if not is_customer(user):
            raise PermissionDenied("Only customers can create properties.")
        serializer.save(owner=user)


class PropertyListView(generics.ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if is_valuer(user):
            return Property.objects.all().order_by("-created_at")
        # customer: only his properties
        return Property.objects.filter(owner=user).order_by("-created_at")


class PropertyDetailView(generics.RetrieveAPIView):
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if is_valuer(user):
            return Property.objects.all()
        return Property.objects.filter(owner=user)
