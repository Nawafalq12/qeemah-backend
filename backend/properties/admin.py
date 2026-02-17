from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "district", "land_type", "legal_document_type", "total_area", "created_at")
    list_filter = ("land_type", "legal_document_type", "has_neighboring_lands")
    search_fields = ("district", "street_name", "owner__username")
