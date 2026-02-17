from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CUSTOMER = "customer"
    ROLE_VALUER = "valuer"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_VALUER, "Valuer"),
        (ROLE_ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    # required ONLY for valuers (we enforce it in serializer)
    valuer_license_no = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
