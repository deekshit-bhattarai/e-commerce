from django.urls import path

from product.admin.views import ProductVariantAdminView

urlpatterns = [
    path(
        "product-variants/",
        ProductVariantAdminView.as_view(),
        name="admin-get-product-variant",
    ),
    path(
        "product-variants/<int:pk>",
        ProductVariantAdminView.as_view(),
        name="admin-get-product-variant",
    ),
]
