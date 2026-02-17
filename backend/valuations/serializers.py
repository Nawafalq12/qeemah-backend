from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import ValuationRequest, ValuationOffer

User = get_user_model()


class ValuationRequestCreateSerializer(serializers.ModelSerializer):
    # العميل يرسل property_id فقط
    property_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ValuationRequest
        fields = ["id", "property_id", "status", "created_at"]
        read_only_fields = ["id", "status", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user

        if user.role != User.ROLE_CUSTOMER:
            raise serializers.ValidationError("فقط العميل (Customer) يقدر يسوي طلب تقييم.")

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        property_id = validated_data.pop("property_id")

        vr = ValuationRequest.objects.create(
            property_id=property_id,
            customer=user,
        )
        return vr


class ValuationRequestListSerializer(serializers.ModelSerializer):
    # نرجع معلومات بسيطة عن العقار
    property = serializers.SerializerMethodField()

    class Meta:
        model = ValuationRequest
        fields = ["id", "property", "status", "created_at"]

    def get_property(self, obj):
        p = obj.property
        return {
            "id": p.id,
            "district": getattr(p, "district", None),
            "street_name": getattr(p, "street_name", None),
            "total_area": getattr(p, "total_area", None),
            "land_type": getattr(p, "land_type", None),
            "legal_document_type": getattr(p, "legal_document_type", None),
        }


class ValuationOfferCreateSerializer(serializers.ModelSerializer):
    request_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ValuationOffer
        fields = ["id", "request_id", "offered_price", "message", "is_selected", "created_at"]
        read_only_fields = ["id", "is_selected", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user

        # لازم يكون Valuer
        if user.role != User.ROLE_VALUER:
            raise serializers.ValidationError("فقط المقيم (Valuer) يقدر يرسل عرض.")

        # لازم تكون عنده رخصة
        if not (user.valuer_license_no or "").strip():
            raise serializers.ValidationError("لازم يكون عندك رقم رخصة عشان ترسل عرض.")

        # الطلب لازم يكون موجود ومفتوح
        request_id = attrs.get("request_id")
        try:
            vr = ValuationRequest.objects.get(id=request_id)
        except ValuationRequest.DoesNotExist:
            raise serializers.ValidationError("طلب التقييم غير موجود.")

        if vr.status != ValuationRequest.STATUS_OPEN:
            raise serializers.ValidationError("هذا الطلب مو مفتوح للعروض.")

        # يمنع تكرار عرض لنفس المقيم على نفس الطلب
        if ValuationOffer.objects.filter(request_id=request_id, valuer=user).exists():
            raise serializers.ValidationError("أنت أرسلت عرض لهذا الطلب مسبقًا.")

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        request_id = validated_data.pop("request_id")

        offer = ValuationOffer.objects.create(
            request_id=request_id,
            valuer=user,
            **validated_data,
        )
        return offer


class ValuationOfferListSerializer(serializers.ModelSerializer):
    valuer = serializers.SerializerMethodField()

    class Meta:
        model = ValuationOffer
        fields = ["id", "valuer", "offered_price", "message", "is_selected", "created_at"]

    def get_valuer(self, obj):
        u = obj.valuer
        return {
            "id": u.id,
            "username": u.username,
            "license_no": u.valuer_license_no,
        }
