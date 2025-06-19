import uuid
from typing import Any

from django.db import models

from commerce.models import UserProfile
from product.models import ProductVariant


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True)
    id = models.BigAutoField(primary_key=True)
    cart_id = models.UUIDField(unique=True, null=True, default=uuid.uuid4)
    # session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        if self.user:
            return f"{self.user}'s Cart"
        return f"Anonymous Cart {self.cart_id}"

    @property
    def total_price(self) -> float:
        return sum(item.item_subtotal for item in self.cartitem_set.all())

    @property
    def items(self) -> Any:
        return self.cartitem_set.all()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_subtotal(self) -> float:
        return self.product.price * self.quantity

    def __str__(self) -> str:
        user_info = (
            self.cart.user.user.email
            if self.cart.user and hasattr(self.cart.user, "user")
            else "anonymous"
        )
        return f"{self.quantity} x {self.product.product.name} in cart of {user_info}"
