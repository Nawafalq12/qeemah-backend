from django.urls import path
from .views import PropertyCreateView, PropertyListView, PropertyDetailView

urlpatterns = [
    path("", PropertyListView.as_view(), name="property-list"),
    path("create/", PropertyCreateView.as_view(), name="property-create"),
    path("<int:pk>/", PropertyDetailView.as_view(), name="property-detail"),
]
