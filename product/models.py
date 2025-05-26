from django.db import models
from django.db.models import Avg, UniqueConstraint
from django.utils.text import slugify

# from commerce.models import UserComment, UserReview


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

    # def total_number_of_comment(self):
    #     return UserComment.objects.filter(product=self).count()
    #
    # def total_number_of_review(self):
    #     return UserReview.objects.filter(product=self).count()
    #
    # def average_product_review(self):
    #     return UserReview.objects.filter(product=self).aggregate(Avg("stars"))[
    #         "stars__avg"
    #     ]

    def __str__(self):
        return self.name


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


# Create your models here.
