from django.contrib import admin

from commerce.models import UserReview
from .models import Category, Product, ProductColor, ProductSize, ProductVariant

class ProductVariantInline(admin.TabularInline):

    """
    Tabular Inline for Product Variants.
    Allows editing ProductVariant objects directly on the Product admin page.
    Includes fields for Size and Color, as they are ForeignKeys on ProductVariant.
    """

    model = ProductVariant
    extra = 1
    fields = (
        "size",
        "color",
        "price",
        "stock",
        "in_stock",
    )

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'on_discount', 'created_at', 'updated_at']
    inlines = [ProductVariantInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'stars', 'review_created_at', 'review_user', 'product']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment', 'created_at', 'updated_at', 'object_id', 'content_type', 'content_object']

# class ProductVariantAdmin(admin.ModelAdmin):
#     list_display = [ 'id', 'product' ]

admin.site.register(ProductVariant)
admin.site.register(Product, ProductAdmin)
admin.site.register(UserReview, ReviewAdmin)
admin.site.register([ProductSize, ProductColor])
admin.site.register(Category )
# Register your models here.
