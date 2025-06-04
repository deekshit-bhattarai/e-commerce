from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from .services import CartService


# Signal to transfer anonymous cart when user logs in
@receiver(user_logged_in)
def transfer_cart_on_login(sender, request, user, **kwargs):
    print()
    print("Signal triggered")
    print()
    """Transfer anonymous cart to user when they log in"""
    user_profile = getattr(user, "userprofile", None)
    if user_profile:
        print("Triggering anonymous cart to user migration...")
        CartService.transfer_anonymous_cart_to_user(request, user_profile)
