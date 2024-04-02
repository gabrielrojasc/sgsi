from __future__ import annotations

from typing import TYPE_CHECKING

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel

if TYPE_CHECKING:
    import datetime

    from documents.models.document_version import DocumentVersion


class Document(BaseModel):
    title = models.CharField(verbose_name=_("title"), max_length=255)
    description = models.TextField(verbose_name=_("description"), blank=True)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self) -> str:
        return self.title

    @property
    def last_version(self) -> DocumentVersion | None:
        return self.versions.order_by("-version").first()

    @property
    def last_approved_version(self) -> DocumentVersion | None:
        return self.versions.approved().order_by("-version").first()

    @property
    def latest_update(self) -> datetime.datetime:
        return max(self.updated_at, self.versions.latest("updated_at").updated_at)

    def get_absolute_url(self) -> str:
        return reverse("document_detail", args=(self.pk,))
