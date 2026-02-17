from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import ValuationRequest, ValuationOffer
from .serializers import (
    ValuationRequestCreateSerializer,
    ValuationRequestListSerializer,
    ValuationOfferCreateSerializer,
    ValuationOfferListSerializer,
)

User = get_user_model()


class ValuationRequestCreateView(generics.CreateAPIView):
    """
    Customer creates a valuation request for a property.
    POST /api/valuations/requests/
    Body: { "property_id": 1 }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ValuationRequestCreateSerializer


class MyValuationRequestsView(generics.ListAPIView):
    """
    Customer views his requests.
    GET /api/valuations/requests/my/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ValuationRequestListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role != User.ROLE_CUSTOMER:
            return ValuationRequest.objects.none()
        return ValuationRequest.objects.filter(customer=user).order_by("-created_at")


class OpenValuationRequestsForValuersView(generics.ListAPIView):
    """
    Valuer views all open requests.
    GET /api/valuations/requests/open/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ValuationRequestListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role not in [User.ROLE_VALUER, User.ROLE_ADMIN]:
            return ValuationRequest.objects.none()
        return ValuationRequest.objects.filter(status=ValuationRequest.STATUS_OPEN).order_by("-created_at")


class ValuationOfferCreateView(generics.CreateAPIView):
    """
    Valuer creates an offer for a request.
    POST /api/valuations/offers/
    Body: { "request_id": 5, "offered_price": 350, "message": "..." }
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ValuationOfferCreateSerializer


class MyOffersView(generics.ListAPIView):
    """
    Valuer views his offers.
    GET /api/valuations/offers/my/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ValuationOfferListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role != User.ROLE_VALUER:
            return ValuationOffer.objects.none()
        return ValuationOffer.objects.filter(valuer=user).order_by("-created_at")


class RequestOffersForCustomerView(generics.ListAPIView):
    """
    Customer views offers for his own request.
    GET /api/valuations/requests/<request_id>/offers/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ValuationOfferListSerializer

    def get_queryset(self):
        user = self.request.user
        request_id = self.kwargs["request_id"]

        vr = get_object_or_404(ValuationRequest, id=request_id)

        if user.role != User.ROLE_CUSTOMER or vr.customer_id != user.id:
            return ValuationOffer.objects.none()

        return ValuationOffer.objects.filter(request=vr).order_by("-created_at")


class ChooseOfferView(APIView):
    """
    Customer chooses one offer.
    POST /api/valuations/offers/<offer_id>/choose/
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, offer_id):
        user = request.user
        offer = get_object_or_404(ValuationOffer, id=offer_id)
        vr = offer.request

        # فقط صاحب الطلب يختار
        if user.role != User.ROLE_CUSTOMER or vr.customer_id != user.id:
            return Response({"detail": "غير مصرح."}, status=status.HTTP_403_FORBIDDEN)

        # لازم الطلب يكون open عشان يختار
        if vr.status != ValuationRequest.STATUS_OPEN:
            return Response({"detail": "الطلب ليس مفتوحًا للاختيار."}, status=status.HTTP_400_BAD_REQUEST)

        # صفّر كل العروض الأخرى
        ValuationOffer.objects.filter(request=vr).update(is_selected=False)

        # اختر هذا العرض
        offer.is_selected = True
        offer.save()

        vr.chosen_offer = offer
        vr.status = ValuationRequest.STATUS_SELECTED
        vr.save()

        return Response({"ok": True, "chosen_offer_id": offer.id})
