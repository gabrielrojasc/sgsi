# Generated by Django 3.2.13 on 2022-05-05 13:39

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
                            ("ip_net", "IP prefix/range"),
                            ("host_list", "host name list"),
                            ("ip_net_list", "IP prefix/range list"),
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
