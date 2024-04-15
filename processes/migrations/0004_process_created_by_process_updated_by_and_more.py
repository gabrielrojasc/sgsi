# Generated by Django 4.2.8 on 2024-04-15 17:11

import django.db.models.deletion

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("processes", "0003_remove_processactivity_completed_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="process",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AddField(
            model_name="process",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AddField(
            model_name="processactivity",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AddField(
            model_name="processactivity",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AddField(
            model_name="processactivitydefinition",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AddField(
            model_name="processactivitydefinition",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
        migrations.AddField(
            model_name="processdefinition",
            name="created_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="created by",
            ),
        ),
        migrations.AddField(
            model_name="processdefinition",
            name="updated_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="updated by",
            ),
        ),
    ]
