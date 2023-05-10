import os

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import TypedDict

import requests


class BaseConfiguration(TypedDict):
    timeout: int
    protocol: str
    host: str


class BaseApiClient(ABC):
    def __init__(self) -> None:
        self.configuration = self.get_configuration()

    def get_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.get(
            url,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def post_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.post(
            url,
            json=body,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def patch_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.patch(
            url,
            json=body,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def put_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.put(
            url,
            json=body,
            params=query_params,
            timeout=self.configuration["timeout"],
        )

    def delete_blocking(
        self,
        endpoint: str,
        path_params: dict[str, Any] | None = None,
    ) -> requests.Response:
        url = self.get_url(endpoint, path_params)
        return requests.delete(
            url,
            timeout=self.configuration["timeout"],
        )

    def get_url(self, endpoint: str, path_params: dict | None = None) -> str:
        parsed_endpoint = self.standarize_url_slashes(endpoint)
        url = os.path.join(self.base_url, parsed_endpoint)
        return url.format(**path_params) if path_params else url

    @staticmethod
    def standarize_url_slashes(url):
        return f"{url.strip('/')}/"

    @property
    def base_url(self) -> str:
        protocol = self.configuration["protocol"]
        host = self.configuration["host"]
        return f"{protocol}://{self.standarize_url_slashes(host)}"

    @abstractmethod
    def get_configuration(self) -> BaseConfiguration:
        ...
