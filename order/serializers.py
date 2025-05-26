from .models import Order
from rest_framework import serializers


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
