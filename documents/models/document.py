from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel
from base.models.versionable_mixin import VersionableMixin
from documents.models.control import Control
from documents.models.document_type import DocumentType

if TYPE_CHECKING:
    from documents.models.document_version import DocumentVersion
    from processes.models.process import Process


class Document(VersionableMixin, BaseModel):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=255,
        unique=True,
    )
    document_type = models.ForeignKey(
        verbose_name=_("document type"),
        to=DocumentType,
        on_delete=models.PROTECT,
        related_name="documents",
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("description"),
        blank=True,
    )
    code = models.CharField(
        verbose_name=_("code"),
        max_length=20,
        unique=True,
        db_index=True,
        help_text=_(
            "The code must have between 3 and 20 uppercase characters and be unique."
        ),
        validators=(
            RegexValidator(
                regex=r"[A-ZÑ\d]{3,20}",
                message=_("Code doesn't comply with required format."),
            ),
        ),
    )
    drive_folder = models.URLField(
        verbose_name=_("drive folder"),
        blank=True,
    )
    documented_controls = models.ManyToManyField(
        verbose_name=_("documented controls"),
        to=Control,
        related_name="documented_in",
        blank=True,
    )

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

    @property
    def last_approved_version(self) -> DocumentVersion | None:
        return self.versions.approved().order_by("-version").first()

    @property
    def can_add_new_versions(self) -> bool:
        return not self.versions.not_approved().exists()

    @property
    def defined_processes(self) -> models.QuerySet[Process]:
        from processes.models.process import Process

        return Process.objects.filter(versions__defined_in=self).distinct()

    def get_absolute_url(self) -> str:
        return reverse("document_detail", args=(self.code,))
