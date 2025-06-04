from rest_framework import routers

from order.views import OrderHistoryView, OrderViewSet, ShippingLocationView

router = routers.DefaultRouter()

router.register(r"order", OrderViewSet, basename="order")
router.register(r"order-history", OrderHistoryView, basename="order-history")
router.register(r"shipping-location", ShippingLocationView, basename="shipping-location")

urlpatterns = []
urlpatterns += router.urls
