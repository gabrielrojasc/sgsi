from http import HTTPStatus

import requests

from api_client.enums import ClientCodes
from api_client.services.client import ApiClientConfiguration
from api_client.services.client import JsonApiClient
from api_client.services.client.auth import BearerAuth


class DummyError(Exception):
    ...


def handle_dummies_fetch(response, error):
    print(response)  # noqa: T201


def handle_dummies_creation(response, error):
    if response.status_code != HTTPStatus.CREATED:
        print("Error creating dummy")  # noqa: T201
    else:
        print(response)  # noqa: T201


def handle_dummies_edition(response, error):
    if response.status_code != HTTPStatus.OK:
        print("Error editing dummy")  # noqa: T201
    else:
        print(response)  # noqa: T201


def handle_dummies_deletion(response, error):
    if response.status_code != HTTPStatus.NO_CONTENT:
        print("Error deleting dummy")  # noqa: T201
    else:
        print("Deleted successfully")  # noqa: T201


def handle_error(response: requests.Response, error):
    print(f"Something happened: {error!s}")  # noqa: T201


class DummyIntegrationService:
    def __init__(self) -> None:
        configuration = ApiClientConfiguration(
            code=ClientCodes.DUMMY_INTEGRATION,
            scheme="http",
            host="localhost:8000/api/v1",
            auth=BearerAuth(
                "thisismagnetbestkeptsecretpleasedonotcopy(c)magnet",
                auth_type="DummyToken",
            ),
        )
        self.api_client = JsonApiClient(configuration)

    def get_dummies(self):
        (data, status_code), error = self.api_client.get_blocking("/dummy/")
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = "Error getting dummies"
            raise DummyError(msg)
        return data

    def get_dummy(self, pk):
        (data, status_code), error = self.api_client.get_blocking(
            "/dummy-auth/{pk}/", path_params={"pk": pk}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = f"Error getting dummy {pk}"
            raise DummyError(msg)
        return data

    def get_dummies_nonblocking(self):
        self.api_client.get(
            "/dummy/",
            on_success=handle_dummies_fetch,
            on_error=handle_error,
        )

    def get_dummy_nonblocking(self, pk):
        self.api_client.get(
            "/dummy/{pk}/",
            path_params={"pk": pk},
            on_success=handle_dummies_fetch,
            on_error=handle_error,
        )

    def create_dummy_nonblocking(self, name):
        self.api_client.post(
            "/dummy/",
            json={"name": name},
            on_success=handle_dummies_fetch,
            on_error=handle_error,
        )

    def update_dummy_nonblocking(self, pk, name):
        self.api_client.put(
            "/dummy/{pk}/",
            path_params={"pk": pk},
            json={"name": name},
            on_success=handle_dummies_edition,
            on_error=handle_error,
        )

    def delete_dummy_nonblocking(self, pk):
        self.api_client.delete(
            "/dummy/{pk}/",
            path_params={"pk": pk},
            on_success=handle_dummies_deletion,
            on_error=handle_error,
        )

    def create_dummy(self, name):
        (data, status_code), error = self.api_client.post_blocking(
            "/dummy/", json={"name": name}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.CREATED:
            msg = f"Error creating dummy {name}"
            raise DummyError(msg)
        return data

    def update_dummy(self, pk, name):
        (data, status_code), error = self.api_client.put_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}, json={"name": name}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = f"Error updating dummy {pk}"
            raise DummyError(msg)
        return data

    def delete_dummy(self, pk):
        (data, status_code), error = self.api_client.delete_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.NO_CONTENT:
            msg = f"Error deleting dummy {pk}"
            raise DummyError(msg)
        return data
