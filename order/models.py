from django.db import models
from commerce.models import UserProfile
from .utils import generate_od_uuid


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
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
    transaction_id = models.CharField(max_length=128)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def price_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x  in Order {self.order.order_id}"
class OrderHistory(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="completion_log"
    )
    completed_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.order.order_id}"
