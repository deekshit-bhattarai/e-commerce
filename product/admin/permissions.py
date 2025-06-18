from rest_framework import permissions
from merchant.permissions import IsMerchant


class IsProductVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return IsMerchant or request.user.parent is not None
