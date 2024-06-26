from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
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

if TYPE_CHECKING:
    from processes.models.process_instance import ProcessInstance
    from users.models.user import User


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
    comment_label = models.CharField(
        verbose_name=_("comment label"),
        max_length=31,
        blank=True,
    )
    recurrency = models.CharField(
        verbose_name=_("recurrency"),
        max_length=255,
        choices=TimeFrameChoices.choices,
        blank=True,
    )
    email_to_notify_completion = models.EmailField(
        verbose_name=_("email to notify completion"),
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
    published_by = models.ForeignKey(
        verbose_name=_("published by"),
        to=settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="published_process_versions",
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
        return f"{self.process} V{self.version}"

    def save(self, *args, **kwargs):
        adding = self._state.adding
        previous_version = self.process.last_published_version
        super().save(*args, **kwargs)
        self._copy_activities_from_previous_version(adding, previous_version)

    def _copy_activities_from_previous_version(
        self, adding: bool, previous_version: ProcessVersion
    ) -> None:
        if not adding or previous_version is None:
            return
        for activity in previous_version.activities.all():
            assignee_groups = tuple(activity.assignee_groups.all())
            activity.pk = None
            activity.process_version = self
            activity.save()
            activity.assignee_groups.set(assignee_groups)

    def _get_increment_queryset(self) -> models.QuerySet[ProcessVersion]:
        return self.process.versions.all()

    def create_first_activity_instance(self, process_instance: ProcessInstance) -> None:
        if self.activities.exists():
            self.activities.earliest("order").create_instance(process_instance)

    def get_absolute_url(self) -> str:
        return reverse("processversion_detail", args=(self.pk,))

    def publish(self, user: User) -> None:
        update_dict = {"is_published": True, "published_at": timezone.now()}
        if user and not user.is_anonymous:
            update_dict["published_by"] = user
        self.update(**update_dict)
