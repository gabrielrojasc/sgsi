# Generated by Django 4.2.8 on 2024-05-17 15:31

from django.db import migrations
from django.db import models


def apply_migration(apps, schema_editor):
    Asset = apps.get_model("information_assets", "Asset")
    for asset in Asset.objects.all():
        code, name = asset.name.split(" ", maxsplit=1)
        asset.code = code
        asset.name = name
        asset.save()


class Migration(migrations.Migration):
    dependencies = [
        ("information_assets", "0004_alter_asset_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="asset",
            name="code",
            field=models.CharField(default="", max_length=20, verbose_name="code"),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="asset",
            options={
                "ordering": ("code",),
                "permissions": (("archive_asset", "Can archive asset"),),
                "verbose_name": "asset",
                "verbose_name_plural": "assets",
            },
        ),
        migrations.RemoveConstraint(
            model_name="asset",
            name="unique_asset_owner",
        ),
        migrations.RunPython(apply_migration, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="asset",
            name="code",
            field=models.CharField(max_length=20, unique=True, verbose_name="code"),
        ),
        migrations.AddConstraint(
            model_name="asset",
            constraint=models.UniqueConstraint(
                fields=("code", "owner"), name="unique_asset_owner"
            ),
        ),
    ]
