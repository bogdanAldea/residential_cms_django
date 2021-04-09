from django.apps import AppConfig


class ResidentialConfig(AppConfig):
    name = 'residential'

    def ready(self):
        import residential.signals
