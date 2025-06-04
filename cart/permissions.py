from rest_framework import permissions
from .models import Cart


class IsOwnerOfCart(permissions.BasePermission):
    """
    Custom permission to only allow owners of a cart to view or edit it.
    Allows anonymous users to access their session-based cart.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            if (
                hasattr(request.user, "userprofile")
                and obj.user == request.user.profile
            ):
                return True
        session_cart_id = request.session.get("cart_id")
        if (
            not request.user.is_authenticated
            and session_cart_id
            and obj.cart_id == session_cart_id
        ):
            return True

        return False

    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        return True
