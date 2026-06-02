from django.apps import AppConfig


class GravesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "graves"

    def ready(self):
        import graves.signals