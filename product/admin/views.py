from rest_framework import generics, status
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from product import serializers
from product.models import ProductVariant
from .serializers import ProductAdminSerializer


class ProductVariantAdminView(
    UpdateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    generics.GenericAPIView,
):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductAdminSerializer

    def get(self, request, pk=None):
        if pk is not None:
            try:
                product = self.get_queryset().get(pk=pk)
            except ProductVariant.DoesNotExist:
                return Response(
                    {"success": False, "message": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            products = self.get_queryset()
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        product = request.data
        serializer = ProductAdminSerializer(data=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            try:
                instance = self.get_queryset().get(pk=pk)
            except ProductVariant.DoesNotExist:
                return Response(
                    {"success": False, "message": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = ProductAdminSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(
                {"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
            )
        except ProductVariant.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
