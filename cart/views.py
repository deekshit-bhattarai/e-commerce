from django.shortcuts import get_object_or_404
from rest_framework import  status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import CartItem
from .serializers import CartReadSerializer, CartWriteSerializer
from .services import CartService


class CartManagementViewSet(viewsets.ViewSet):
    """
    Combined ViewSet for comprehensive cart management
    """

    def list(self, request):
        """GET /cart-management/ - Get current cart with all items"""
        cart = CartService.get_or_create_cart(request)
        serializer = CartReadSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """POST /cart-management/add_item/ - Add item to cart"""
        product_variant_id = request.data.get("product_variant_id")
        quantity = request.data.get("quantity", 1)

        try:
            cart_item = CartService.add_to_cart(request, product_variant_id, quantity)
            cart = CartService.get_or_create_cart(request)
            serializer = CartWriteSerializer(cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["patch"])
    def update_item(self, request):
        """PATCH /cart-management/update_item/ - Update cart item"""
        cart_id = request.session.get("cart_id")
        quantity = int(request.data.get("quantity"))
        item_id = request.data.get("item_id")

        if not item_id:
            return Response(
                {"error": "item_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not cart_id:
            return Response(
                {"error": "cart_item_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = CartService.get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem.objects.filter(cart=cart), pk=item_id)

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity += quantity
            cart_item.save()

        from .serializers import CartWriteSerializer

        serializer = CartWriteSerializer(cart, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["delete"])
    def remove_item(self, request):
        """DELETE - /api/remove_item/ - Remove item from cart"""
        request_item_quantity = int(request.data.get("quantity"))
        item_id = request.data.get("item_id")

        if not request_item_quantity:
            return Response(
                {"error": "Quantity field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not item_id:
            return Response(
                {"error": "`item_id` field is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cart = CartService.get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem.objects.filter(cart=cart), id=item_id)

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity -= request_item_quantity
            cart_item.save()

        from .serializers import CartWriteSerializer

        serializer = CartWriteSerializer(cart, context={"request": request})
        return Response(serializer.data)
