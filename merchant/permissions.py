from rest_framework.permissions import BasePermission 

class IsMerchant(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name="Merchant").exists() and request.user.is_merchant


class IsMerchantOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user and request.user.is_authenticated
        is_merchant = request.user.groups.filter(name="Merchant").exists() and getattr(request.user, "is_merchant", False)
        is_superuser = getattr(request.user, "is_superuser", False)
        return is_authenticated and (is_merchant or is_superuser)
