from rest_framework import serializers
from django.contrib.auth import get_user_model

from merchant.models import Merchant

User = get_user_model()


class SubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        parent_user = self.context["request"].user

        # Create the user
        user = User.objects.create(**validated_data, parent=parent_user)

        try:
            parent_merchant = Merchant.objects.get(owner=parent_user)
        except Merchant.DoesNotExist:
            raise serializers.ValidationError(
                "Merchant entry for the current user not found."
            )

        return user


class MerchantSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    subusers = SubUserSerializer(source="owner.sub_user", many=True, read_only=True)

    class Meta:
        model = Merchant
        fields = [
            "id",
            "name",
            "description",
            "created_at",
            "updated_at",
            "owner",
            "subusers",
        ]

    def create(self, validated_data):
        user = Merchant.objects.create(**validated_data)
        return user
