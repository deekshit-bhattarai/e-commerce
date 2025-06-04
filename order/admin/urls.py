
from rest_framework import routers

from .views import AdminOrderViewSet, AdminUserViewSet

router = routers.DefaultRouter()

router.register(r"admin/users", AdminUserViewSet, basename="admin-users")
router.register(r"admin/orders", AdminOrderViewSet, basename="admin-orders")

urlpatterns = []
urlpatterns += router.urls
