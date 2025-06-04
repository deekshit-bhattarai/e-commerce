from rest_framework import viewsets
from django.contrib.auth import get_user_model

from order.models import Order
from .serializers import AdminOrderSerializer, AdminUserSerializer
from .permissions import IsAdminUser

User = get_user_model()

class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdminUser]
