from django.shortcuts import render
from .serializers import OrderReadSerializer
from .models import Order
from rest_framework import mixins, viewsets, permissions


class OrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create your views here.
