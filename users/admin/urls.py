from rest_framework import routers
from .views import AdminUserViewSet

router = routers.DefaultRouter()


router.register(r"admin/users", AdminUserViewSet, basename="admin-users")

urlpatterns = router.urls
