from django.apps import AppConfig
from project import settings

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    
    def ready(self):
        import app.signals
        # if settings.SCHEDULER_DEFAULT:
        #     from project import operator
        #     operator.start()