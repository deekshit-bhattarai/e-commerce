from rest_framework import status, viewsets
from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin, UpdateModelMixin
from rest_framework.response import Response

from order.models import Order
from .serializers import AdminOrderSerializer
from .permissions import IsSuperAdminUser

User = get_user_model()


class AdminOrderViewSet(ListModelMixin, UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = AdminOrderSerializer
    permission_classes = [IsSuperAdminUser]
    lookup_field = "order_id"

    def get(self, request, pk=None, *args, **kwargs):
        if pk is not None:
            try:
                order = self.get_queryset().get(pk=pk)
            except Order.DoesNotExist:
                return Response(
                    {"message": "Order doesn't exist"}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            order = self.get_queryset()
            serializer = self.get_serializer(order, many=True)
            return Response(
                {
                    "success": True,
                    "message": "Got all order successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
