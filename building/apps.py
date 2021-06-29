from django.apps import AppConfig


class BuildingConfig(AppConfig):
    name = 'building'

    def ready(self):
        import building.signals
