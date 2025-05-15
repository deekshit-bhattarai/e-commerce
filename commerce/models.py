from typing import override
from uuid import uuid4

from django.conf import settings
from django.db import models


def generate_od_uuid():
    """
    Generates a random 8-character string prefixed with 'od_'.

    Uses UUID4 to generate a random UUID, takes the first 8 characters
    of its hexadecimal representation, and prepends 'od_'.

    Returns:
        str: A string in the format 'od_xxxxxxxx' where xxxxxxxx is
             8 random hexadecimal characters.
    """
    # Generate a random UUID (version 4)
    random_uuid = uuid4()

    # Get the hexadecimal representation of the UUID and take the first 8 characters
    short_uuid = str(random_uuid).replace("-", "")[:8]

    # Prefix with 'od_'
    prefixed_uuid = f"od_{short_uuid}"

    return prefixed_uuid


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.email


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)

    @property
    def in_stock(self):
        self.stock > 0

    def __str__(self):
        return f"{self.name} "


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        REFUND = "Refund"
        CANCEL = "Cancelled"
        FAILED = "Failed"
        PROCESSING = "Processing"

    order_id = models.CharField(primary_key=True, default=generate_od_uuid())
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=15, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity

    @override
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart of {self.cart.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def price_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"