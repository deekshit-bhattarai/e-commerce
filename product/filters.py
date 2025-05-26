import django_filters

from .models import ProductVariant

# class InStockFilterBackend(filters.BaseFilterBackend):
#     @override
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(stock__gt=0)


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = ProductVariant
        fields = {
            "price": ["exact", "lt", "gt", "range"],
            "product__category__name": ["icontains", "exact"],
        }


# class OrderFilter(django_filters.FilterSet):
#
#     created_at = django_filters.DateFilter(field_name="created_at__date")
#
#     class Meta:
#         model = Order
#         fields = {
#             "status": ["exact"],
#             "created_at": ["lt", "gt", "exact"],
#         }
