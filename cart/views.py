from django.shortcuts import render
from rest_framework.decorators import action
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from rest_framework import viewsets, status


from rest_framework.response import Response
from .services import CartService
from .models import CartItem


class CartViewSet(viewsets.GenericViewSet):
    def get_cart(self):
        return CartService.get_or_create_cart(self.request)

    @action(detail=False, methods=["get"])
    def my_cart(self, request):
        cart = self.get_cart()
        print()
        print(cart)
        print()
        cart_data = {
            "cart_id": str(cart.cart_id),
            "items": [
                {
                    "id": item.id,
                    "product": {
                        "id": item.product.id,
                        "name": item.product.product.name,
                        "price": float(item.product.price),
                        "size": item.product.size.size,
                        "color": item.product.color.color,
                    },
                    "quantity": item.quantity,
                    "subtotal": float(item.item_subtotal),
                }
                for item in cart.cartitem_set.all()
            ],
            "total_price": float(cart.total_price),
            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
        }
        return Response(cart_data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        product_variant_id = request.data.get("product_variant_id")
        quantity = request.data.get("quantity", 1)

        if not product_variant_id:
            return Response(
                {"error": "Product variant id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            CartService.add_to_cart(request, product_variant_id, quantity)
            cart = self.get_cart()

            return self.my_cart(request)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["patch"])
    def update_item(self, request):
        """Update cart item quantity"""
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity")

        if not item_id or quantity is None:
            return Response(
                {"error": "item_id and quantity are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = self.get_cart()

        try:
            item = cart.cartitem_set.get(id=item_id)

            if quantity <= 0:
                item.delete()
            else:
                item.quantity = quantity
                item.save()

            return self.my_cart(request)

        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=["delete"])
    def remove_item(self, request):
        """Remove item from cart"""
        item_id = request.data.get("item_id")

        if not item_id:
            return Response(
                {"error": "item_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart()

        try:
            item = cart.cartitem_set.get(id=item_id)
            item.delete()
            return self.my_cart(request)

        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
            )


# Signal to transfer anonymous cart when user logs in
@receiver(user_logged_in)
def transfer_cart_on_login(sender, request, user, **kwargs):
    """Transfer anonymous cart to user when they log in"""
    user_profile = getattr(user, "userprofile", None)
    if user_profile:
        CartService.transfer_anonymous_cart_to_user(request, user_profile)
