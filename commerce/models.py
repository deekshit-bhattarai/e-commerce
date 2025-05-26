from typing import override
from django.db.models.signals import post_save
import uuid
from django.dispatch import receiver

from django.conf import settings
from django.db import models
from product import models as product_app_model


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.email


class UserComment(models.Model):
    comment = models.CharField(max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="comment_user"
    )
    product = models.ForeignKey(
        product_app_model.Product,
        on_delete=models.CASCADE,
        related_name="user_product_comment",
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
        product_app_model.Product,
        on_delete=models.CASCADE,
        related_name="user_product_review",
    )

    def __str__(self):
        return f"{self.review_user.user}'s Review"


@receiver(post_save, sender=UserProfile)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
