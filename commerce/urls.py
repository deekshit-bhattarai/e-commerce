from django.urls import path
from rest_framework import routers

from commerce import views

router = routers.SimpleRouter()
router.register(r"categories", views.CategoryListViewSet)
router.register(r"product-variant", views.ProductVariantViewSet)
router.register(r"thumbnail", views.ProductThumbnailListViewSet)
router.register(r"", views.ProductListViewSet, basename="product-list-viewset")

urlpatterns = []
urlpatterns += router.urls
