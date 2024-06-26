# Generated by Django 4.2.8 on 2024-04-29 14:13

import django.db.models.deletion

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("processes", "0003_alter_processversion_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="processactivityinstance",
            name="asignee_group",
        ),
        migrations.RemoveField(
            model_name="processactivityinstance",
            name="description",
        ),
        migrations.RemoveField(
            model_name="processactivityinstance",
            name="order",
        ),
        migrations.AddField(
            model_name="processversion",
            name="published_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="published_process_versions",
                to=settings.AUTH_USER_MODEL,
                verbose_name="published by",
            ),
        ),
    ]
