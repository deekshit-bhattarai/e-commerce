from rest_framework import viewsets
from django.contrib.auth import get_user_model

from order.models import Order
from .serializers import AdminOrderSerializer
from .permissions import IsAdminUser

User = get_user_model()



class AdminOrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = AdminOrderSerializer
    permission_classes = [IsAdminUser]
