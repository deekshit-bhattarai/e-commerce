from typing import override
from django.contrib.auth import user_logged_in
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

    def create(self, validated_data) -> UserProfile:
        val_pass = validated_data.pop("password")
        password = make_password(val_pass)
        user = UserProfile.objects.create(
            email=validated_data["email"], password=password
        )
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)

    @override
    def validate(self, attrs):
        data = super().validate(attrs)

        if self.user and self.context.get("request"):
            request = self.context["request"]
            user_logged_in.send(
                sender=self.user.__class__, request=request, user=self.user
            )
            print(
                f"DEBUG : user_logged_in signal dispatched for {self.user.email} during JWT obtain"
            )

        else:
            print(
                f"DEBUG: Could not dispatch user_logged_in signal. User: {self.user}, Request: {self.context.get('request')}"
            )

        return data


# class JWTSerializer(JSONWebTokenSerializer):
#     def validate(self, attrs):
#         credentials = {
#             self.email_field: attrs.get(self.email_field),
#             "password": attrs.get("password"),
#         }
#
#         if all(credentials.values()):
#             user = authenticate(request=self.context["request"], **credentials)
#
#             if user:
#                 if not user.is_active:
#                     msg = "User account disabled"
#                     raise serializers.ValidationError(msg)
#
#                 payload = jwt_payload_handler(user)
#                 user_logged_in.send(
#                     sender=user.__class__, request=self.context["request"], user=user
#                 )
#
#                 return {"token": jwt_encoder(payload), "user": user}
#
#             else:
#                 msg = "Unable to login with provided credentials."
#                 raise serializers.ValidationError(msg)
#
#         else:
#             msg = f'Must include {self.email_field} and "password".'
#             raise serializers.ValidationError(msg)
