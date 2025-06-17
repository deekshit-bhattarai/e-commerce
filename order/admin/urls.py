from rest_framework import routers

from .views import AdminOrderViewSet

router = routers.DefaultRouter()

router.register(r"orders", AdminOrderViewSet, basename="admin-orders")

urlpatterns = []
urlpatterns += router.urls
