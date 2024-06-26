# Generated by Django 4.2.8 on 2024-05-16 19:46

from django.db import migrations
from django.db import models

import documents.models.document_version


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0008_documentversion_approval_evidence"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="documentversion",
            options={
                "ordering": ("-version",),
                "permissions": (
                    ("approve_documentversion", "Can approve document version"),
                    (
                        "view_documentversion_verification_code",
                        "Can view document version verification code",
                    ),
                ),
                "verbose_name": "document version",
                "verbose_name_plural": "document versions",
            },
        ),
        migrations.AddField(
            model_name="documentversion",
            name="verification_code",
            field=models.CharField(
                default=documents.models.document_version.generate_verification_code,
                editable=False,
                max_length=8,
                verbose_name="verification code",
            ),
        ),
    ]
