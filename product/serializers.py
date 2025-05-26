from .models import Product, ProductColor, ProductSize, ProductVariant, Category
from commerce.models import UserProfile, UserComment, UserReview
from rest_framework import serializers


class CategoryReadSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "slug", "parent", "children"]
        read_only_fields = [
            "id",
            "slug",
        ]

    def get_children(self, obj):
        children_queryset = obj.children.all().filter(parent=obj.id)
        serializer = self.__class__(children_queryset, many=True)

        return serializer.data


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "description", "parent"]


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["id", "size"]


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ["id", "color"]


class ProductVariantWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    size = serializers.PrimaryKeyRelatedField(queryset=ProductSize.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=ProductColor.objects.all())

    class Meta:
        model = ProductVariant
        fields = ["id", "product", "size", "color", "stock", "in_stock"]
        read_only_fields = ["id"]


class UserProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["user_email", "address"]

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None


class ProductCommentReadSerializer(serializers.ModelSerializer):
    comment_user = UserProfileSerializer()

    class Meta:
        model = UserComment
        fields = ["id", "created_at", "comment_user", "comment"]
        read_only_fields = ["id", "created_at", "comment_user", "comment"]


class ProductReviewReadSerializer(serializers.ModelSerializer):
    review_user = UserProfileSerializer()

    class Meta:
        model = UserReview
        fields = "__all__"


class ProductThumbnailListReadSerializer(serializers.ModelSerializer):
    average_review_stars = serializers.SerializerMethodField()
    total_number_of_review = serializers.SerializerMethodField()
    total_number_of_comment = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            # "id",
            "name",
            "description",
            "category",
            "average_review_stars",
            "total_number_of_review",
            "total_number_of_comment",
        ]

    def get_average_review_stars(self, obj):
        return obj.average_product_review()

    #
    def get_total_number_of_review(self, obj):
        return obj.total_number_of_review()

    #
    def get_total_number_of_comment(self, obj):
        return obj.total_number_of_comment()


class ProductReadSerializer(serializers.ModelSerializer):
    user_product_comment = ProductCommentReadSerializer(many=True, read_only=True)
    user_product_review = ProductReviewReadSerializer(many=True, read_only=True)
    category = CategoryReadSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "on_discount",
            "discount_price",
            "created_at",
            "updated_at",
            "user_product_comment",
            "user_product_review",
        ]
        read_only_fields = [
            "created_at",
            "id",
            "updated_at",
        ]


class ProductVariantReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)
    size = ProductSizeSerializer(read_only=True)
    color = ProductColorSerializer(read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "product", "price", "size", "color", "stock", "in_stock"]
        read_only_fields = [
            "id",
            "product",
            "price",
            "size",
            "color",
            "stock",
            "in_stock",
        ]


# class ProductWriteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ["name", "description", "stock", "category"]
#
#     def validate_price(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("The price must be above 0")
#         return value
