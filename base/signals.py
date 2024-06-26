from django.conf import settings

# base imports
from base.middleware import RequestMiddleware
from base.utils import get_our_models


class NotExists:
    """
    This class represents no data available for a given dict key.
    It is required because `None` may be a valid value.
    """


def audit_log(sender, instance, created, raw, update_fields=None, **kwargs):
    """
    Post save signal that creates a log when an object from a models from
    our apps is created or updated.
    """
    # only listening models created in our apps
    if sender not in get_our_models():
        return

    sensitive_fields = settings.LOG_SENSITIVE_FIELDS
    ignored_fields = settings.LOG_IGNORE_FIELDS
    user = get_user()

    if raw:
        return

    if created:
        message = {
            "added": instance.to_dict(
                exclude=ignored_fields + sensitive_fields,
                include_m2m=False,
            ),
        }
        instance._save_addition(user, message)
    else:
        changed_field_labels = {}
        original_dict = instance.original_dict
        actual_dict = instance.to_dict(exclude=ignored_fields, include_m2m=False)
        keys_to_check = update_fields if update_fields else original_dict.keys()

        for key in keys_to_check:
            if original_dict.get(key, NotExists) != actual_dict.get(key, NotExists):
                if key in sensitive_fields:
                    changed_field_labels[key] = "field updated"
                else:
                    changed_field_labels[key] = {
                        "from": original_dict[key],
                        "to": actual_dict[key],
                    }
        if changed_field_labels:
            message = {"changed": {"fields": changed_field_labels}}
            instance._save_edition(user, message)


def audit_delete_log(sender, instance, **kwargs):
    """
    Post delete signal that creates a log when an object from a models from
    our apps is deleted.
    """
    # only listening models created in our apps
    if sender not in get_our_models():
        return
    user = get_user()
    instance._save_deletion(user)


def get_user():
    thread_local = RequestMiddleware.thread_local
    return thread_local.user if hasattr(thread_local, "user") else None
