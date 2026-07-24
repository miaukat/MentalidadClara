from django.apps import AppConfig

class MentalidadAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mentalidad_app'

    def ready(self):
        import mentalidad_app.signals  # Importa y activa las señales al arrancar