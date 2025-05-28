from django.contrib import admin

from .models import Order, OrderHistory, OrderItem, ShippingLocation


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ["order", "completed_by", "completed_at"]


admin.site.register([Order, OrderItem, ShippingLocation])
admin.site.register(OrderHistory, OrderHistoryAdmin)

# Register your models here.
