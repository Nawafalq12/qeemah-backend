from django.contrib import admin
from .models import ValuationRequest, ValuationOffer


@admin.register(ValuationRequest)
class ValuationRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "customer", "status", "chosen_offer", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username",)


@admin.register(ValuationOffer)
class ValuationOfferAdmin(admin.ModelAdmin):
    list_display = ("id", "request", "valuer", "offered_price", "is_selected", "created_at")
    list_filter = ("is_selected", "created_at")
    search_fields = ("valuer__username",)
