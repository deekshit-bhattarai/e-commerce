from django.contrib import admin
from .models import (
    UserComment,
    UserProfile,
    UserReview,
)


# class ProductVariantInline(admin.TabularInline):

#     """
#     Tabular Inline for Product Variants.
#     Allows editing ProductVariant objects directly on the Product admin page.
#     Includes fields for Size and Color, as they are ForeignKeys on ProductVariant.
#     """
#
#     model = ProductVariant
#     extra = 1
#     fields = (
#         "size",
#         "color",
#         "price",
#         "stock",
#         "in_stock",
#     )
#
#
# class ProductCommentInline(admin.TabularInline):
#
#     model = UserComment
#     extra = 1
#
#
# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 1
#
#
# class ProductAdmin(admin.ModelAdmin):
#     inlines = [
#         ProductCommentInline,
#         ProductVariantInline,
#         ProductImageInline,
#     ]
#
#
# admin.site.register(
#     [Category, ProductColor, ProductSize, Cart, CartItem, UserComment, UserReview]
# )
# admin.site.register(Product, ProductAdmin)
# admin.site.register(UserProfile)
