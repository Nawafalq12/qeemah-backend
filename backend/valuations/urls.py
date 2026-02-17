from django.urls import path
from .views import (
    ValuationRequestCreateView,
    MyValuationRequestsView,
    OpenValuationRequestsForValuersView,
    ValuationOfferCreateView,
    MyOffersView,
    RequestOffersForCustomerView,
    ChooseOfferView,
)

urlpatterns = [
    # Requests
    path("requests/", ValuationRequestCreateView.as_view(), name="valuation-request-create"),
    path("requests/my/", MyValuationRequestsView.as_view(), name="valuation-request-my"),
    path("requests/open/", OpenValuationRequestsForValuersView.as_view(), name="valuation-request-open"),

    # Offers
    path("offers/", ValuationOfferCreateView.as_view(), name="valuation-offer-create"),
    path("offers/my/", MyOffersView.as_view(), name="valuation-offer-my"),

    # Customer sees offers for a request
    path("requests/<int:request_id>/offers/", RequestOffersForCustomerView.as_view(), name="valuation-request-offers"),

    # Customer chooses offer
    path("offers/<int:offer_id>/choose/", ChooseOfferView.as_view(), name="valuation-offer-choose"),
]
