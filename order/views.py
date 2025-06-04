from typing import override

from rest_framework import mixins, permissions, viewsets

from commerce.models import UserProfile

from .models import Order, OrderHistory, ShippingLocation
from .serializers import OrderHistorySerializer, OrderReadSerializer


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = OrderReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=user_profile)
        return Order.objects.none()


class OrderHistoryView(viewsets.GenericViewSet, mixins.ListModelMixin):
    # queryset = OrderHistory.objects.all()
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        if self.request.user.is_authenticated:
            return OrderHistory.objects.filter(user=user_profile)


class ShippingLocationView(viewsets.GenericViewSet):
    queryset = ShippingLocation

