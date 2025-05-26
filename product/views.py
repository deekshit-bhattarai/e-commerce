from django_filters import rest_framework as filters
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import ProductFilter
from .models import Category, Product, ProductVariant
from .serializers import (
    CategoryReadSerializer,
    CategoryWriteSerializer,
    ProductThumbnailListReadSerializer,
    ProductVariantReadSerializer,
    ProductVariantWriteSerializer,
)


class CategoryListViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().filter(parent__isnull=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CategoryReadSerializer
        return CategoryWriteSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [permissions.AllowAny()]
        elif self.request.method == "POST":
            return [permissions.IsAdminUser()]
        return super().get_permissions()


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all().select_related("product")
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

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
    queryset = ProductVariant.objects.all().order_by("pk")
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


class ProductThumbnailListViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("pk")
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductThumbnailListReadSerializer
        if self.action in ["update", "create", "partial_update"]:
            return Response({"message": "write stuff"}, status=status.HTTP_200_OK)
