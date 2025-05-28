from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order, OrderHistory


@receiver(post_save, sender=Order)
def order_to_history_save_handler(sender, instance, created, **kwargs):
    # breakpoint()
    if not created and instance.status.lower() == "completed":
        if not hasattr(instance, "completion_log"):
            OrderHistory.objects.create(order=instance, completed_by=instance.user)
