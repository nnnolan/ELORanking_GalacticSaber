from django.apps import AppConfig
import django.contrib.admin
import django.contrib.auth, django.contrib.contenttypes, django.contrib.messages, django.contrib.sessions 


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'login'