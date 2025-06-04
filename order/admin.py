from django.contrib import admin

from .models import Order, OrderHistory, OrderItem, ShippingLocation


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ["order", "completed_by", "completed_at"]


class ShippingLocationAdmin(admin.ModelAdmin):
    list_display = [
        "recepient_name",
        "phone_no",
        "st_name",
        "city",
        "province",
        "country",
    ]


admin.site.register([Order, OrderItem])
admin.site.register(OrderHistory, OrderHistoryAdmin)
admin.site.register(ShippingLocation)

# Register your models here.
