# Generated by Django 4.2.8 on 2024-03-20 14:00

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0002_control_document"),
    ]

    operations = [
        migrations.AlterField(
            model_name="controlcategory",
            name="name",
            field=models.CharField(max_length=255, unique=True, verbose_name="name"),
        ),
    ]