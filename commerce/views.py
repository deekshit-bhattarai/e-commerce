from typing import override
import uuid

from rest_framework.response import Response
from rest_framework import generics, status, views, viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.serializers import Serializer

from commerce.models import CartItem, Category, Order, Product, ProductVariant
from commerce.serializers import (
    CartItemReadSerializer,
    CategoryReadSerializer,
    CategoryWriteSerializer,
    ProductReadSerializer,
    ProductThumbnailListReadSerializer,
    ProductVariantReadSerializer,
    ProductVariantWriteSerializer,
    ProductWriteSerializer,
)


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all().select_related("product", "size", "color")
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductVariantReadSerializer
        return ProductVariantWriteSerializer

    @action(detail=False, methods=["get"])
    def by_product(self, request, pk=None):
        product_id = request.query_params.get("product_id")
        if not product_id:
            return Response(
                {"detail": "`product_id` parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            product = Product.objects.get(pk=product_id)
            variants = product.variants.all()
            serializer = self.get_serializer(variants, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProductListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by("pk")
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductVariantReadSerializer
        if self.action in ["create", "update", "partial_update"]:
            return ProductVariantWriteSerializer

    def get_queryset(self):
        return super().get_queryset()

    queryset = ProductVariant.objects.all().order_by("pk")


class ProductThumbnailListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("pk")
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductThumbnailListReadSerializer
        if self.action in ["update", "create", "partial_update"]:
            return Response({"message": "write stuff"}, status=status.HTTP_200_OK)


class CategoryListViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().filter(parent__isnull=True)
    permission_classes = [permissions.IsAuthenticated]

    @override
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategoryReadSerializer
        return CategoryWriteSerializer

    @override
    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        elif self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class CartItemReadViewSet(viewsets.ModelViewSet):
    @override
    def get_queryset(self):
        queryset = CartItem.objects.all()
        user = self.request.user
        cart_id = self.request.query_params.get("cart_id")
        if user.is_authenticated:
            return queryset.filter(cart__user__user=user)
        elif user.is_anonymous:
            cart_uuid = uuid.UUID(cart_id)
            return CartItem.objects.filter(cart_cart_id=cart_uuid)

    @override
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CartItemReadSerializer
        return CategoryWriteSerializer
