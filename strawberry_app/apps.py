from django.apps import AppConfig


class StrawberryAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "strawberry_app"

    def ready(self):
        from strawberry_app.views import create_cultures

        create_cultures()


class UserConfig(AppConfig):
    name = "users"

    def ready(self):
        import strawberry_app.signals
