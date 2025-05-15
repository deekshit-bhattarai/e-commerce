from rest_framework import serializers
from .models import Order, Product


class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "stock", "image"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("The price must be above 0")
        return value


class OrderReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
