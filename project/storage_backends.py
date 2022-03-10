from django.conf import settings
from storages.backends import s3boto3


class S3StaticStorage(s3boto3.S3StaticStorage):
    location = "static"
    default_acl = "public-read"

    def __init__(self, **_settings):
        super().__init__(**_settings)

        if settings.DO_SPACES_CDN_ENABLED:
            # The CDN replies much faster (16ms vs 450ms), but the first GET takes around 1s.

            # Use the CDN for public files only.
            # For private files which have a non-constant signature, the CDN is actually slower.

            # If the faster speed of the CDN is preferred for media, delete the "private" acl
            # and this `if` block, and globally set AWS_S3_CUSTOM_DOMAIN.

            self.custom_domain = (
                f"{settings.AWS_STORAGE_BUCKET_NAME}"
                f".{settings.DO_SPACES_REGION}.cdn.digitaloceanspaces.com")


class S3MediaStorage(s3boto3.S3Boto3Storage):
    location = "media"
    default_acl = "private"
    file_overwrite = False
