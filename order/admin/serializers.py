from django.contrib.auth import get_user_model
from rest_framework import serializers

from order.models import Order

User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_active" , "is_staff", "is_superadmin"]

class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
