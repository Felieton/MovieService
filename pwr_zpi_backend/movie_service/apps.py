from django.apps import AppConfig


class MovieServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movie_service'

    def ready(self):
        # looks insane but it is required for signals to work
        from . import signals
