from django.conf import settings
from django.db import models


class ValuationRequest(models.Model):
    STATUS_OPEN = "open"
    STATUS_SELECTED = "selected"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_SELECTED, "Selected"),
        (STATUS_CLOSED, "Closed"),
    ]

    # الطلب مرتبط بالعقار
    property = models.ForeignKey(
        "properties.Property",
        on_delete=models.CASCADE,
        related_name="valuation_requests",
    )

    # صاحب الطلب (العميل)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="valuation_requests",
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)

    # العرض المختار (اختياري)
    chosen_offer = models.ForeignKey(
        "ValuationOffer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chosen_for_requests",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request#{self.id} | property={self.property_id} | customer={self.customer_id} | {self.status}"


class ValuationOffer(models.Model):
    # العرض تابع لطلب
    request = models.ForeignKey(
        ValuationRequest,
        on_delete=models.CASCADE,
        related_name="offers",
    )

    # المقيم الذي قدم العرض
    valuer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="valuation_offers",
    )

    # مبلغ العرض (كم ياخذ مقابل التقييم)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)

    # ملاحظات المقيم (اختياري)
    message = models.TextField(blank=True, default="")

    # هل تم اختيار هذا العرض؟
    is_selected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # يمنع نفس المقيم يقدم أكثر من عرض لنفس الطلب
        constraints = [
            models.UniqueConstraint(fields=["request", "valuer"], name="uniq_offer_per_request_per_valuer")
        ]

    def __str__(self):
        return f"Offer#{self.id} | req={self.request_id} | valuer={self.valuer_id} | {self.offered_price}"
