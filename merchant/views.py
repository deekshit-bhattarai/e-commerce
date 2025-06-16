from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework import status

from merchant.models import Merchant
from merchant.permissions import IsMerchant
from merchant.serializers import MerchantSerializer, SubUserSerializer

User = get_user_model()

class MerchantView(viewsets.ModelViewSet):
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return Merchant.objects.all()
            return Merchant.objects.filter(owner=user)
        return Merchant.objects.none()

    @action(detail = True, methods = ["post"], url_path="add-to-group")
    def add_to_group(self, request, *args, **kwargs):

        try:
            merchant = self.get_object()
        except Http404:
            return Response({'error' : 'Merchant not found'}, status=status.HTTP_404_NOT_FOUND)

        user = merchant.owner
        group_name = request.data.get('group')
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            return Response({"status" : "user added to group"})
        except Group.DoesNotExist:
            return Response({'error' : 'Group not found'}, status=status.HTTP_400_BAD_REQUEST)

class SubUserViewSet(viewsets.ModelViewSet):
    serializer_class = SubUserSerializer
    permission_classes = [IsMerchant]

    def get_queryset(self):
        return User.objects.filter(parent=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(parent=self.request.user)
