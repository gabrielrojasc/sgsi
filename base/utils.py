""" Small methods for generic use """


import os
import re

from itertools import cycle

from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils import numberformat
from django.utils import timezone

# others libraries

RUT_FILTER_RE = re.compile("[^0-9kK]")


def today():
    """
    This method obtains today"s date in local time
    """
    return timezone.localtime(timezone.now()).date()


def format_rut(rut):
    if not rut:
        return ""

    rut = re.sub(RUT_FILTER_RE, "", rut)
    if not rut:
        return ""

    if len(rut) < 2:  # noqa: PLR2004
        msg = "RUTs must have at least two digits"
        raise ValueError(msg)

    digits, verifier = int(rut[:-1]), rut[-1]
    code = numberformat.format(
        digits,
        ",",
        decimal_pos=0,
        grouping=3,
        thousand_sep=".",
        force_grouping=True,
        use_l10n=False,
    )

    return f"{code}-{verifier}"


def rut_verifying_digit(rut):
    """
    Uses a mod11 algorithm to compute RUT's check digit.
    Returns a value from 0 to 9 or k.
    """

    rev = map(int, reversed(str(rut)))
    factors = cycle(range(2, 8))
    s = sum(d * f for d, f in zip(rev, factors, strict=False))
    mod = (-s) % 11
    return "0123456789k"[mod]


def validate_rut(rut):
    rut = rut.strip().lower()
    rut = re.sub(RUT_FILTER_RE, "", rut)

    if len(rut) < 2:  # noqa: PLR2004
        return False

    aux, dv = rut[:-1], rut[-1]
    res = rut_verifying_digit(aux)

    return res == dv


def get_our_models():
    for model in apps.get_models():
        app_label = model._meta.app_label

        # test only those models that we created
        if os.path.isdir(app_label):
            yield model


def can_loginas(request, target_user):
    """This will only allow admins to log in as other users"""
    return (
        request.user.is_superuser
        and not target_user.is_superuser
        and target_user.is_active  # users not active cannot log in
    )


def get_slug_fields(model):
    slug_fields = []
    for field in model._meta.fields:
        if isinstance(field, models.SlugField):
            slug_fields.append(field)
    return slug_fields


def build_absolute_url_wo_req(path: str) -> str:
    """
    Returns an absolute URL to an absolute `path` (like `/admin/`).
    If you have a `request`, use
    [build_absolute_uri](http://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest.build_absolute_uri)
    instead.
    """
    # django
    from django.contrib.sites.models import Site

    scheme = "https" if settings.SECURE_SSL_REDIRECT else "http"
    site = Site.objects.get_current()
    return f"{scheme}://{site.domain}{path}"


def get_subclasses(cls):
    """Inspects a model and returns its subclass list.

    (See: https://stackoverflow.com/a/29106313)
    """
    result = {cls}
    to_inspect = [cls]
    while to_inspect:
        class_to_inspect = to_inspect.pop()
        for subclass in class_to_inspect.__subclasses__():
            if subclass not in result:
                result.add(subclass)
                to_inspect.append(subclass)
    return result
