# Generated by Django 3.2.18 on 2023-06-02 19:54

from django.db import migrations
from django.db import models

import base.mixins
import base.serializers


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ClientConfig",
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
                (
                    "client_code",
                    models.CharField(
                        choices=[("DUMMY_INTEGRATION", "Dummy Integration")],
                        max_length=255,
                        unique=True,
                        verbose_name="client code",
                    ),
                ),
                ("enabled", models.BooleanField(default=True, verbose_name="enabled")),
                (
                    "retries",
                    models.PositiveIntegerField(default=0, verbose_name="retries"),
                ),
            ],
            options={
                "verbose_name": "client configuration",
                "verbose_name_plural": "clients configurations",
            },
            bases=(base.mixins.AuditMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ClientLog",
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
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("GET", "GET"),
                            ("POST", "POST"),
                            ("PUT", "PUT"),
                            ("PATCH", "PATCH"),
                            ("DELETE", "DELETE"),
                        ],
                        max_length=10,
                        verbose_name="method",
                    ),
                ),
                ("url", models.TextField(verbose_name="url")),
                ("endpoint", models.TextField(verbose_name="endpoint")),
                ("client_url", models.TextField(verbose_name="client url")),
                (
                    "client_code",
                    models.TextField(
                        choices=[("DUMMY_INTEGRATION", "Dummy Integration")],
                        verbose_name="client code",
                    ),
                ),
                (
                    "request_time",
                    models.DateTimeField(
                        help_text="request time", null=True, verbose_name="request time"
                    ),
                ),
                (
                    "request_headers",
                    models.JSONField(
                        default=dict,
                        encoder=base.serializers.StringFallbackJSONEncoder,
                        verbose_name="headers",
                    ),
                ),
                ("request_content", models.TextField(verbose_name="content")),
                (
                    "response_time",
                    models.DateTimeField(
                        help_text="response time",
                        null=True,
                        verbose_name="response time",
                    ),
                ),
                (
                    "response_headers",
                    models.JSONField(
                        default=dict,
                        encoder=base.serializers.StringFallbackJSONEncoder,
                        verbose_name="headers",
                    ),
                ),
                ("response_content", models.TextField(verbose_name="content")),
                (
                    "response_status_code",
                    models.IntegerField(null=True, verbose_name="status code"),
                ),
                ("error", models.TextField(verbose_name="error")),
                (
                    "error_email_sent",
                    models.BooleanField(default=False, verbose_name="error email sent"),
                ),
            ],
        ),
    ]