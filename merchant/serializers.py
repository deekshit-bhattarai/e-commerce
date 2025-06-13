from rest_framework import serializers
from django.contrib.auth import get_user_model

from merchant.models import Merchant

User = get_user_model()

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = "__all__"

class SubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
