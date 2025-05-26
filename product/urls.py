from rest_framework import routers
from .views import (
    CategoryListViewSet,
    ProductListViewSet,
    ProductThumbnailListViewSet,
    ProductVariantViewSet,
)

router = routers.SimpleRouter()
router.register(r"categories", CategoryListViewSet)
router.register(r"product-variant", ProductVariantViewSet)
router.register(r"product-thumbnail", ProductThumbnailListViewSet)
router.register(r"product-list", ProductListViewSet, basename="product-list-viewset")

urlpatterns = []
urlpatterns += router.urls
