from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from base.models.base_model import BaseModel
from base.models.version_mixin import VersionModelBase
from documents.models.control import Control
from documents.models.document import Document
from processes.enums import TimeFrameChoices
from processes.managers import ProcessVersionQuerySet
from processes.models.process import Process


class ProcessVersion(VersionModelBase, BaseModel):
    process = models.ForeignKey(
        verbose_name=_("process"),
        to=Process,
        on_delete=models.PROTECT,
        related_name="versions",
    )
    defined_in = models.ForeignKey(
        verbose_name=_("defined in"),
        to=Document,
        on_delete=models.PROTECT,
        related_name="processes",
    )
    controls = models.ManyToManyField(
        verbose_name=_("controls"),
        to=Control,
        related_name="process_versions",
    )
    recurrency = models.CharField(
        verbose_name=_("recurrency"),
        max_length=255,
        choices=TimeFrameChoices.choices,
        blank=True,
    )
    is_published = models.BooleanField(
        verbose_name=_("published"),
        default=False,
    )
    published_at = models.DateTimeField(
        verbose_name=_("published at"),
        null=True,
        blank=True,
    )

    objects = ProcessVersionQuerySet.as_manager()

    class Meta:
        verbose_name = _("process version")
        verbose_name_plural = _("process versions")
        permissions = (("publish_processversion", "Can publish process version"),)

    @property
    def can_be_updated(self) -> bool:
        return not self.is_published

    def __str__(self) -> str:
        return f"{self.process}  V{self.version}"

    def _get_increment_queryset(self) -> models.QuerySet[ProcessVersion]:
        return self.process.versions.all()

    def get_absolute_url(self) -> str:
        return reverse("processversion_detail", args=(self.pk,))

    def publish(self) -> None:
        self.update(is_published=True, published_at=timezone.now())
