# class CartItemReadViewSet(viewsets.ModelViewSet):
#     @override
#     def get_queryset(self):
#         breakpoint()
#         queryset = CartItem.objects.all()
#         user = self.request.user
#         cart_id = self.request.query_params.get("cart_id")
#         if user.is_authenticated:
#             return queryset.filter(cart__user__user=user)
#         elif user.is_anonymous:
#             cart_uuid = uuid.UUID(cart_id)
#             return CartItem.objects.filter(cart_cart_id=cart_uuid)
#
#     @override
#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return CartItemReadSerializer
#         return CategoryWriteSerializer
