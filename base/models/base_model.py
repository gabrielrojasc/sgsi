import json

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.mixins import AuditMixin
from base.serializers import ModelEncoder
from base.utils import build_absolute_url_wo_req


class BaseModel(AuditMixin, models.Model):
    """An abstract class that every model should inherit from"""

    BOOLEAN_CHOICES = ((False, _("No")), (True, _("Yes")))

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("creation date"),
        verbose_name=_("created at"),
    )
    created_by = models.ForeignKey(
        verbose_name=_("created by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        help_text=_("edition date"),
        verbose_name=_("updated at"),
    )
    updated_by = models.ForeignKey(
        verbose_name=_("updated by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    # field used to store a dictionary with the instance original fields
    original_dict = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_dict = self.to_dict(
            exclude=settings.LOG_IGNORE_FIELDS,
            include_m2m=False,
        )

    def _save_addition(self, user, message):
        if user and not user.is_anonymous:
            self.update(created_by=user, updated_by=user, skip_save=True)
        return super()._save_addition(user, message)

    def _save_edition(self, user, message):
        if user and not user.is_anonymous:
            self.update(updated_by=user, skip_save=True)
        return super()._save_edition(user, message)

    # public methods
    def update(self, skip_save=False, **kwargs):
        """
        This is a shortcut method, it basically sets all keyword arguments as
        attributes on the calling object, then it stores only those values
        into the database.

        To store values into the database, this method uses the `save` method
        with the `update_fields` parameter, but if you want to skip the save
        method, you can pass the parameter `skip_save=True` when calling update
        (useful when you want to avoid calling save signals).
        """
        kwargs["updated_at"] = timezone.now()

        for kw in kwargs:
            self.__setattr__(kw, kwargs[kw])

        if skip_save:
            self.__class__.objects.filter(pk=self.pk).update(**kwargs)
        else:
            self.save(update_fields=kwargs.keys())

    def to_dict(self, fields=None, exclude=None, include_m2m=True):
        """
        Returns a dict containing the data in ``instance``

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.
        """

        opts = self._meta
        data = {}
        for f in opts.fields + opts.many_to_many:
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, models.fields.related.ForeignKey):
                data[f.attname] = self.__dict__.get(f.attname)
            elif isinstance(f, models.fields.related.ManyToManyField):
                if include_m2m:
                    # If the object doesn't have a primary key yet, just use an
                    # emptylist for its m2m fields. Calling f.value_from_object
                    # will raise an exception.
                    if self.pk is None:
                        data[f.name] = []
                    else:
                        # MultipleChoiceWidget needs a list of pks, not objects
                        data[f.name + "_ids"] = list(
                            getattr(self, f.attname).values_list("pk", flat=True),
                        )
            else:
                data[f.name] = self.__dict__.get(f.name)
        return data

    def to_json(self, fields=None, exclude=None, **kargs):
        """
        Returns a string containing the data in of the instance in json format

        ``fields`` is an optional list of field names. If provided, only the
        named fields will be included in the returned dict.

        ``exclude`` is an optional list of field names. If provided, the named
        fields will be excluded from the returned dict, even if they are listed
        in the ``fields`` argument.

        kwargs are optional named parameters for the json.dumps method
        """
        # obtain a dict of the instance data
        data = self.to_dict(fields=fields, exclude=exclude)

        # turn the dict to json
        return json.dumps(data, cls=ModelEncoder, **kargs)

    def get_full_url(self):
        return build_absolute_url_wo_req(self.get_absolute_url())
