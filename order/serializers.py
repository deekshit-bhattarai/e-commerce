from .models import Order, OrderHistory, ShippingLocation
from rest_framework import serializers


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]


class OrderHistorySerializer(serializers.ModelSerializer):
    completed_by = serializers.SerializerMethodField()

    class Meta:
        model = OrderHistory
        fields = ["id", "order", "completed_by", "completed_at"]

    def get_completed_by(self, obj):
        return obj.completed_by.user.email if obj.completed_by else None

class ShippingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingLocation
        fields = "__all__"
        read_only_fields = [ "user" ]
