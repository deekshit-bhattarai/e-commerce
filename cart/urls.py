from rest_framework import routers

from .views import CartManagementViewSet

router = routers.SimpleRouter()
# router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart", CartManagementViewSet, basename="cart")

urlpatterns = []
urlpatterns += router.urls
