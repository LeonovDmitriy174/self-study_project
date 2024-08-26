from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("swagger<format>/", schema_view.without_ui(), name="schema-json"),
    path(
        "swagger/",
        schema_view.with_ui("swagger"),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc"), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls"), name="materials"),
    path("materials/", include("materials.urls"), name="materials"),
]
