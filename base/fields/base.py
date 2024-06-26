"""
Custom Fields
"""

from django.core.exceptions import ValidationError
from django.db.models import CharField
from django.db.models import FileField

# translations
from django.utils.translation import gettext_lazy as _

# utils
from base import utils

from .functions import file_path


class ChileanRUTField(CharField):
    """
    A model field that stores a Chilean RUT in the format "XX.XXX.XXX-Y".
    Letters are stored in uppercase.
    """

    description = _("Chilean RUT (up to %(max_length)s)")
    default_error_messages = {
        "invalid": _(
            "'%(value)s' is an invalid RUT.",
        ),
        "invalid_type": _("'%(value)s' must be str or None."),
    }

    def __init__(self, *args, **kwargs):
        if "max_length" not in kwargs:
            kwargs["max_length"] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not (isinstance(value, str) or value is None):
            raise ValidationError(
                self.error_messages["invalid_type"],
                code="invalid",
                params={"value": value},
            )

        value = str(value).strip()
        if not value:
            return value

        if not utils.validate_rut(value):
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid",
                params={"value": value},
            )

        return utils.format_rut(value)


class BaseFileField(FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("upload_to", file_path)
        super().__init__(*args, **kwargs)
