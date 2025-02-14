from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserAuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_apps.user_auth'
    verbose_name = _('User Auth')
