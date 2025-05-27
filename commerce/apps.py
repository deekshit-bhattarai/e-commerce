from typing import override
from django.apps import AppConfig


class CommerceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "commerce"

    @override
    def ready(self) -> None:
        import commerce.signals
