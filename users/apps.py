from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .permissions import IsAuthenticatedAndHasPermission
        from .signals import assign_user_permissions
