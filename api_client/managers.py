from django.conf import settings
from django.db import models
from django.utils import timezone

from api_client.enums import ClientCodes


class ClientLogQueryset(models.QuerySet):
    def old(self):
        days = settings.CLIENT_LOG_AGE_IN_DAYS_FOR_DELETION
        deletion_time = timezone.now() - timezone.timedelta(days=days)
        return self.filter(created_at__lt=deletion_time)


class DisabledClientQueryset(models.QuerySet):
    def is_disabled(self, client_code: ClientCodes):
        return self.filter(client_code=client_code).exists()
