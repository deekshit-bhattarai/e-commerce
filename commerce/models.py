from typing import override
import uuid
from django.db.models import Avg, UniqueConstraint, constraints
from uuid import uuid4
from django.utils.text import slugify

from django.conf import settings
from django.db import models
from django.db.models.fields import related


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


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.email


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="children",
    )

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["-name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductSize(models.Model):

    size = models.CharField(max_length=210, unique=True)

    def __str__(self):
        return self.size


class ProductColor(models.Model):

    color = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.color


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    on_discount = models.BooleanField()
    discount_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    # color = models.ForeignKey(ProductColor, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ["-created_at"]

    @property
    def in_stock(self):
        return self.variants.filter(stock__gt=0).exists()

    def total_number_of_comment(self):
        return UserComment.objects.filter(product=self).count()

    def total_number_of_review(self):
        return UserReview.objects.filter(product=self).count()

    def average_product_review(self):
        return UserReview.objects.filter(product=self).aggregate(Avg("stars"))[
            "stars__avg"
        ]

    def __str__(self):
        return self.name


class UserComment(models.Model):
    comment = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="comment_user"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="user_product_comment"
    )

    def __str__(self):
        return f"{self.comment_user.user} | {self.product.name}"


class UserReview(models.Model):
    REVIEW_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    stars = models.IntegerField(choices=REVIEW_CHOICES, max_length=10)
    review_comment = models.CharField(max_length=600)
    review_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    review_created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="user_product_review"
    )

    def __str__(self):
        return f"{self.review_user.user}'s Review"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["product", "size", "color"], name="unique_product_variant"
            )
        ]

    def __str__(self):
        return f"{self.price}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.FileField("API/product_images", max_length=100, null=True)


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def price_subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    cart_id = models.UUIDField(unique=True, null=True, default=uuid.uuid4)

    def __str__(self):
        return f"{self.user}'s Cart"


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
