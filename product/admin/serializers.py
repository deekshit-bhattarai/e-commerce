from rest_framework import serializers
from product.models import ProductVariant


class ProductAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "price",
            "product",
            "stock",
            "in_stock",
            "size",
            "color",
        ]
