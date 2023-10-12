from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AutoservisasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autoservisas'
    verbose_name = _('user profile')