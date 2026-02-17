from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def ping(request):
    return JsonResponse({"ok": True})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ping/", ping),

    path("api/auth/", include("accounts.urls")),
    path("api/properties/", include("properties.urls")),
    path("api/valuations/", include("valuations.urls")),
]
