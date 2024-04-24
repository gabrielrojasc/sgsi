# Generated by Django 4.2.8 on 2024-04-24 17:01

import django.db.models.deletion

from django.conf import settings
from django.db import migrations
from django.db import models

import base.mixins


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("documents", "0002_alter_documentversion_version"),
        ("processes", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="processactivity",
            options={
                "ordering": ("process_version", "order"),
                "verbose_name": "process activity",
                "verbose_name_plural": "process activities",
            },
        ),
        migrations.RemoveField(
            model_name="process",
            name="control",
        ),
        migrations.RemoveField(
            model_name="process",
            name="recurrency",
        ),
        migrations.RemoveField(
            model_name="processactivity",
            name="process",
        ),
        migrations.RemoveField(
            model_name="processinstance",
            name="control",
        ),
        migrations.RemoveField(
            model_name="processinstance",
            name="name",
        ),
        migrations.RemoveField(
            model_name="processinstance",
            name="process",
        ),
        migrations.CreateModel(
            name="ProcessVersion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="creation date",
                        verbose_name="created at",
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="edition date",
                        null=True,
                        verbose_name="updated at",
                    ),
                ),
                ("version", models.PositiveSmallIntegerField(verbose_name="version")),
                (
                    "recurrency",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("DAILY", "Daily"),
                            ("WEEKLY", "Weekly"),
                            ("MONTHLY", "Monthly"),
                            ("QUARTERLY", "Quarterly"),
                            ("SEMIANNUALLY", "Semiannually"),
                            ("ANNUALLY", "Annually"),
                        ],
                        max_length=255,
                        verbose_name="recurrency",
                    ),
                ),
                (
                    "controls",
                    models.ManyToManyField(
                        related_name="process_versions",
                        to="documents.control",
                        verbose_name="control",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "defined_in",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="processes",
                        to="documents.document",
                        verbose_name="defined in",
                    ),
                ),
                (
                    "process",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="versions",
                        to="processes.process",
                        verbose_name="process",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "process version",
                "verbose_name_plural": "process versions",
            },
            bases=(base.mixins.AuditMixin, models.Model),
        ),
        migrations.AddField(
            model_name="processactivity",
            name="process_version",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="activities",
                to="processes.processversion",
                verbose_name="process version",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="processinstance",
            name="process_version",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="instances",
                to="processes.processversion",
                verbose_name="process version",
            ),
            preserve_default=False,
        ),
    ]
