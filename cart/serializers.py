from rest_framework import serializers
from .models import CartItem, Cart
from product.models import Product, ProductVariant
from product.serializers import CategoryReadSerializer


class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductVariantForCartSerializer(
    #     read_only=True,
    # )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )
    product_detail = serializers.StringRelatedField(source="product", read_only=True)
    category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "price",
            "item_subtotal",
            "product",
            "product_detail",
            "quantity",
            "category",
        ]

    def create(self, validated_data) -> CartItem:
        cart = self.context.get("cart")
        if not cart:
            raise serializers.ValidationError(
                "Cart context not created for CartItem creation"
            )
        product_data = validated_data.pop("product")
        product_id = product_data.get("product.id")

        if not product_id:
            raise serializers.ValidationError(
                "Product ID is required for Cart Item creation"
            )
        try:
            product = ProductVariant.objects.get(id=product_id)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("Product Variant doesn't exist")

        # Checking if product already exists in the cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": validated_data.get("quantity", 1)},
        )

        if not created:
            cart_item.quantity += validated_data.get("quantity", 1)
            cart_item.save()

        return cart_item

    def get_category(self, obj):
        return CategoryReadSerializer(obj.product.product.category).data

    def get_price(self, obj):
        return obj.product.price if obj.product else None


class CartReadSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source="cartitem_set", many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["cart_id", "total_price", "items", "created_at", "updated_at"]


class CartWriteSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["cart_id", "total_price", "items", "created_at", "updated_at"]

    def create(self, validated_data) -> Cart:
        # breakpoint()
        items_data = validated_data.pop("items", [])
        cart = Cart.objects.create(**validated_data)

        for item_data in items_data:
            product_id = None

            if "product_id" in item_data:
                product_id = item_data.pop("product_id")
            elif "product" in item_data:
                product_data = item_data.pop("product")
                product_id = product_data.id

            if not product_id:
                raise serializers.ValidationError(
                    "Product ID is required for CartItem creation"
                )

            try:
                product: ProductVariant = ProductVariant.objects.get(id=product_id)
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError(
                    f"Product Variant with ID {product_id} doesn't exist"
                )

            CartItem.objects.create(cart=cart, product=product, **item_data)

        return cart

    def update(self, instance, validated_data):
        instance.cart_id = validated_data.get("cart_id", instance.cart_id)
        instance.save()

        # Change this line:
        incoming_items_data = validated_data.pop("items", None)

        if incoming_items_data is not None:
            # Get current cart items related to this cart instance
            current_cart_items = {
                item.product.id: item for item in instance.items.all()
            }

            # Track product IDs from incoming data to identify items to delete
            incoming_product_ids = set()

            for item_data in incoming_items_data:
                # 'product' in item_data will be the ProductVariant instance due to source='product'
                product_variant = item_data.pop("product")
                quantity = item_data.get("quantity", 1)

                incoming_product_ids.add(product_variant.id)

                # Check if this item already exists in the cart
                if product_variant.id in current_cart_items:
                    # Item exists, update its quantity
                    cart_item = current_cart_items[product_variant.id]
                    cart_item.quantity = (
                        quantity  # Or += quantity, depending on desired behavior
                    )
                    cart_item.save()
                    print(
                        f"Updated CartItem: {cart_item.id} (Product: {product_variant.id}) quantity to {quantity}"
                    )
                else:
                    # Item does not exist, create a new one
                    CartItem.objects.create(
                        cart=instance, product=product_variant, quantity=quantity
                    )
                    print(
                        f"Created new CartItem for Product: {product_variant.id} with quantity {quantity}"
                    )

            # 3. Delete items that are no longer in the incoming data
            # Find product IDs that are in current_cart_items but not in incoming_product_ids
            products_to_delete_ids = (
                set(current_cart_items.keys()) - incoming_product_ids
            )

            for product_id in products_to_delete_ids:
                cart_item_to_delete = current_cart_items[product_id]
                cart_item_to_delete.delete()
                print(
                    f"Deleted CartItem: {cart_item_to_delete.id} (Product: {product_id})"
                )

        return instance
