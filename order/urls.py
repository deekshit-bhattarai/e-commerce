from rest_framework import routers

from order.views import OrderViewSet

router = routers.SimpleRouter()

router.register(r"order", OrderViewSet, basename="order")

urlpatterns = []
urlpatterns += router.urls
