from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_protocol(value):
    if value not in {"http", "https", "magnet"}:
        raise ValidationError(_("Invalid protocol"))
