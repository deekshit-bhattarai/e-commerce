from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    address = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_merchant = models.BooleanField(default=False)
    belongs_to = models.CharField(max_length=100, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="sub_user",
    )

    # profile_image = models.ImageField("API/profile-images", default=)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email
