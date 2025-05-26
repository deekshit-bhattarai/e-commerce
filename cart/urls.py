from rest_framework import routers

from .views import CartViewSet

router = routers.SimpleRouter()
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = []
urlpatterns += router.urls
