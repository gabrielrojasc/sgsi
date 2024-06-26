from django.conf import settings

import requests

from api_client.enums import ClientCodes

from ..config import ApiClientConfiguration
from ..errors import ClientConfigurationError


class BaseApiClient:
    """
    General methods for API clients.

    You should not use this class directly. Use BlockingApiClient, NonBlockingApiClient
    or ApiClient instead.
    """

    empty_response = requests.Response()

    def __new__(cls, *args, **kwargs):
        if cls is BaseApiClient:
            msg = "This class is not meant to be used directly. Use ApiClient instead."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init__(self, configuration: ApiClientConfiguration) -> None:
        self.configuration = configuration
        self.validate_configuration()

    def validate_configuration(self) -> None:
        self.validate_client_code()
        self.validate_timeout()

    def validate_client_code(self):
        try:
            ClientCodes(self.configuration.code)
        except ValueError as e:
            msg = f"Invalid client code: {self.configuration.code}"
            raise ClientConfigurationError(msg) from e

    def validate_timeout(self) -> None:
        if self.configuration.timeout > settings.API_CLIENT_MAX_TIMEOUT:
            msg = (
                f"Can't set timeout at {self.configuration.timeout}s, the max is "
                f"{settings.API_CLIENT_MAX_TIMEOUT}s"
            )
            raise ClientConfigurationError(msg)
