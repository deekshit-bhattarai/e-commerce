from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = UserProfile
        fields = ["email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords doesn't match")
        if "password2" in attrs:
            attrs.pop("password2")
        return attrs

    def create(self, validated_data):
        val_pass = validated_data.pop("password")
        password = make_password(val_pass)
        user = UserProfile.objects.create(
            email=validated_data["email"], password=password
        )
        return user

