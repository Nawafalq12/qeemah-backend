from django.conf import settings
from django.db import models


class Property(models.Model):
    # صاحب العقار (العميل)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="properties",
    )

    # نوع الوثيقة
    DOC_DEED = "deed"
    DOC_REGISTRY = "registry"
    LEGAL_DOCUMENT_CHOICES = [
        (DOC_DEED, "Electronic Deed (صك إلكتروني)"),
        (DOC_REGISTRY, "Real Estate Registry (سجل عقاري)"),
    ]
    legal_document_type = models.CharField(
        max_length=20,
        choices=LEGAL_DOCUMENT_CHOICES,
        default=DOC_DEED,
    )

    # نوع الأرض
    LAND_RESIDENTIAL = "residential"
    LAND_COMMERCIAL = "commercial"
    LAND_AGRICULTURAL = "agricultural"
    LAND_INDUSTRIAL = "industrial"
    LAND_TYPE_CHOICES = [
        (LAND_RESIDENTIAL, "Residential (سكني)"),
        (LAND_COMMERCIAL, "Commercial (تجاري)"),
        (LAND_AGRICULTURAL, "Agricultural (زراعي)"),
        (LAND_INDUSTRIAL, "Industrial (صناعي)"),
    ]
    land_type = models.CharField(max_length=20, choices=LAND_TYPE_CHOICES)

    # الموقع
    district = models.CharField(max_length=120)     # الحي
    street_name = models.CharField(max_length=120)  # اسم الشارع

    # المساحة الكلية
    total_area = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # طول الواجهة على الشارع (بالمتر)
    street_front_length_m = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # هل فيه أراضي مجاورة؟
    has_neighboring_lands = models.BooleanField(default=False)

    # من أي جهة توجد أراضي مجاورة؟
    # (اختياري: نفعّله فقط لو has_neighboring_lands = True)
    neighboring_north = models.BooleanField(default=False)
    neighboring_south = models.BooleanField(default=False)
    neighboring_east = models.BooleanField(default=False)
    neighboring_west = models.BooleanField(default=False)

    # عرض الشوارع المحيطة (لو ما فيه شارع من جهة معيّنة خلّها 0)
    north_street_width = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    south_street_width = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    east_street_width = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    west_street_width = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Property #{self.id} - {self.district}"
