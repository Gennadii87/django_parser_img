from django.apps import AppConfig


class MyParserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'my_parser'

    def ready(self):
        import my_parser.signals
