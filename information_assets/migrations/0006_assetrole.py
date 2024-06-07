# Generated by Django 4.2.13 on 2024-06-07 15:20

import django.db.models.deletion

from django.conf import settings
from django.db import migrations
from django.db import models

import base.mixins


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("information_assets", "0005_asset_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="AssetRole",
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
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "asset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="roles",
                        to="information_assets.asset",
                        verbose_name="asset",
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
                "verbose_name": "asset role",
                "verbose_name_plural": "asset roles",
                "unique_together": {("asset", "name")},
            },
            bases=(base.mixins.AuditMixin, models.Model),
        ),
    ]
