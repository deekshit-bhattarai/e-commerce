from uuid import uuid4

from django.db import models

from commerce.models import UserProfile

from .utils import generate_od_uuid


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        COMPLETED = "Completed"
        REFUND = "Refund"
        CANCEL = "Cancelled"
        FAILED = "Failed"
        PROCESSING = "Processing"

    order_id = models.CharField(
        primary_key=True, default=generate_od_uuid(), unique=True
    )
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    transaction_id = models.UUIDField(default=uuid4())

    def __str__(self):
        return f"{self.user} | {self.order_id} | {self.status} | {self.transaction_id}"


class OrderItem(models.Model):
    from product.models import ProductVariant

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def price_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.id} | {self.product.product.name} | {self.quantity} | {self.price} | {self.price_subtotal}"


class OrderHistory(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="completion_log"
    )
    completed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.order.order_id}"


class ShippingLocation(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    st_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    receipent_name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        parts = []
        parts.append(self.st_name)
        if self.city:
            parts.append(self.city)
        if self.province:
            parts.append(self.province)
        if self.country:
            parts.append(self.country)

        return f"{self.id} | {self.user}'s shipping location : {', '.join(parts)} received by {self.receipent_name}"
