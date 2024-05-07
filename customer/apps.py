from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer'


class ClienteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cliente'


class InterventoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'intervento'
