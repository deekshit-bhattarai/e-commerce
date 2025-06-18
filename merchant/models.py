from django.conf import settings
from django.db import models


class Merchant(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=600)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name = 'merchant'
    )

    def __str__(self):
        return f"ID : {self.id} | Merchant name : {self.name} | Merchant e-mail : {self.owner}"

