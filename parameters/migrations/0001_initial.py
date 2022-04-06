# Generated by Django 3.2.12 on 2022-04-05 22:58

import base.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Parameter",
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
                ("raw_value", models.TextField(verbose_name="value")),
                (
                    "name",
                    models.CharField(
                        editable=False, max_length=50, unique=True, verbose_name="name"
                    ),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("int", "integer"),
                            ("time", "time"),
                            ("date", "date"),
                            ("json", "json"),
                            ("url", "url"),
                            ("host", "host name"),
                            ("bool", "boolean"),
                            ("str", "text"),
                        ],
                        editable=False,
                        max_length=255,
                        verbose_name="kind",
                    ),
                ),
                (
                    "cache_seconds",
                    models.PositiveIntegerField(
                        default=3600, verbose_name="cache seconds"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=(base.mixins.AuditMixin, models.Model),
        ),
    ]
