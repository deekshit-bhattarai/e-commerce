from rest_framework import serializers
from product.serializers import ProductReadSerializer
from .models import CartItem, Cart
from product.models import ProductVariant


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "item_subtotal"]

    def create(self, validated_data):
        cart = self.context["cart"]
        product_id = validated_data.pop("product.id")
        product = ProductVariant.objects.get(id=product_id)

        # Checking if product already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": validated_data.get("quantity", 1)},
        )

        if not created:
            cart_item.quantity += validated_data.get("quantity", 1)
            cart_item.save()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer()

    class Meta:
        model = Cart
        fields = ["cart_id", "items", "created_at", "updated_at"]
