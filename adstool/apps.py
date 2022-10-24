from django.apps import AppConfig


class AdstoolConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adstool'
    def ready(self):
        import adstool.signals