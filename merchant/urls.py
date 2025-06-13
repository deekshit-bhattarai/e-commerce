
from merchant.views import MerchantView, SubUserViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"merchants", MerchantView, basename="merchant")
router.register(r"sub-user", SubUserViewSet, basename="sub-user")

urlpatterns = []

urlpatterns += router.urls
