from typing import override

from rest_framework import mixins, permissions, viewsets

from commerce.models import UserProfile

from .models import Order, OrderHistory, ShippingLocation
from .serializers import OrderHistorySerializer, OrderReadSerializer, ShippingLocationSerializer


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


class ShippingLocationView(
    mixins.ListModelMixin,      # For GET (list)
    mixins.CreateModelMixin,    # For POST
    mixins.RetrieveModelMixin,  # For GET with ID
    mixins.UpdateModelMixin,    # For PUT/PATCH
    mixins.DestroyModelMixin, 
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ShippingLocationSerializer

    @override
    def get_queryset(self):
        user = UserProfile.objects.get(user=self.request.user)
        return ShippingLocation.objects.filter(user = user)

    def perform_create(self, serializer):
        user = UserProfile.objects.get(user=self.request.user)
        return serializer.save(user=user)

    def perform_update(self, serializer):
        user = UserProfile.objects.get(user=self.request.user)
        instance = serializer.save()
        if instance.is_active:
            ShippingLocation.objects.filter(user=user).exclude(id=instance.id).update(is_active=False)


    
