from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.db.models.signals import post_delete
from django.db.models.signals import post_save


class BaseConfig(AppConfig):
    name = "base"

    def ready(self):
        # Register post_save and post_delete handlers
        from base import signals
        from base.models import BaseModel
        from base.utils import get_subclasses

        for subclass in get_subclasses(BaseModel):
            if subclass._meta.abstract or subclass._meta.proxy:
                continue

            post_save.connect(
                signals.audit_log,
                sender=subclass,
                dispatch_uid=subclass.__name__.lower() + "_post_save",
            )
            post_delete.connect(
                signals.audit_delete_log,
                sender=subclass,
                dispatch_uid=subclass.__name__.lower() + "_post_delete",
            )


class BaseAdminConfig(AdminConfig):
    default_site = "base.admin_site.BaseAdminSite"
