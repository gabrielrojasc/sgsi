# Generated by Django 4.2.8 on 2024-05-01 23:19


import django.db.models.deletion

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("processes", "0005_remove_processactivity_asignee_xor_asignee_group_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="processactivity",
            old_name="asignee_group",
            new_name="assignee_group",
        ),
        migrations.RenameField(
            model_name="processactivityinstance",
            old_name="asignee",
            new_name="assignee",
        ),
        migrations.AddField(
            model_name="processactivity",
            name="email_to_notify",
            field=models.EmailField(
                blank=True, max_length=254, verbose_name="email to notify"
            ),
        ),
        migrations.AlterField(
            model_name="processactivity",
            name="assignee_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="activities",
                to="auth.group",
                verbose_name="assignee group",
            ),
        ),
        migrations.AlterField(
            model_name="processactivityinstance",
            name="assignee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="activity_instances",
                to=settings.AUTH_USER_MODEL,
                verbose_name="assignee",
            ),
        ),
    ]
