from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model to use email as base identifier instead of username for authentication
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save user with given email and password
        """

        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have `is_staff = True`")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have `is_superuser = True`")
        return self.create_user(email, password, **extra_fields)
