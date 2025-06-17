from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.response import Response

from product import serializers
from product.models import ProductVariant
from .serializers import ProductAdminSerializer


class ProductVariantAdminView(
    UpdateModelMixin, ListModelMixin, CreateModelMixin, generics.GenericAPIView
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
            return Response(serializer.data)
        else:
            products = self.get_queryset()
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        product = request.data
        serializer = ProductAdminSerializer(data=product)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = ProductAdminSerializer(instance, request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response
