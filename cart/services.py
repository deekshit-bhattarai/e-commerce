from uuid import uuid4

from .models import Cart, CartItem
from product.models import ProductVariant


class CartService:
    @staticmethod
    def get_or_create_cart(request):
        if request.user.is_authenticated:
            user_profile = getattr(request.user, "userprofile", None)
            if user_profile:
                cart, created = Cart.objects.get_or_create(user=user_profile)
                return cart

        breakpoint()
        cart_id = request.session.get("cart_id")
        # breakpoint()
        if not request.session.get("cart_id"):
            cart_id = str(uuid4())
            request.session["cart_id"] = cart_id
            request.session.save()

        cart, created = Cart.objects.get_or_create(
            cart_id=cart_id,
            user=None,
        )
        return cart

    @staticmethod
    def transfer_anonymous_cart_to_user(request, user_profile):
        cart_id = request.session.get("cart_id")
        if not cart_id:
            return None

        try:
            anonymous_cart = Cart.objects.get(cart_id=cart_id, user=None)
            user_cart, created = Cart.objects.get_or_create(user=user_profile)

            for item in anonymous_cart.cartitem_set.all():
                existing_item = user_cart.cartitem_set.filter(
                    product=item.product
                ).first()

                if existing_item:
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    CartItem.objects.create(
                        cart=user_cart, product=item.product, quantity=item.quantity
                    )
            anonymous_cart.delete()
            return user_cart
        except Cart.DoesNotExist:
            return Cart.objects.get_or_create(user=user_profile)[0]

    @staticmethod
    def add_to_cart(request, product_variant_id, quantity=1):
        try:
            product_variant = ProductVariant.objects.get(id=product_variant_id)
            cart = CartService.get_or_create_cart(request)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product_variant, defaults={"quantity": quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return cart_item
        except ProductVariant.DoesNotExist:
            raise ValueError("Requested product variant doesn't exist")
