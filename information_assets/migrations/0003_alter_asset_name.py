# Generated by Django 4.2.8 on 2024-05-10 19:58

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        ("information_assets", "0002_asset_is_archived"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="name",
            field=models.CharField(max_length=63, verbose_name="name"),
        ),
    ]
