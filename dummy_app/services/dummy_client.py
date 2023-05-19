from http import HTTPStatus

from api_client.services import BaseJsonApiClient


class DummyError(Exception):
    ...


class DummyClient(BaseJsonApiClient):
    def get_extra_configuration(self) -> dict:
        return {
            "host": "localhost:8000/api/v1",
            "scheme": "http",
        }

    def get_dummies(self):
        (data, status_code), error = self.get_blocking("/dummy/")
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = "Error getting dummies"
            raise DummyError(msg)
        return data

    def get_dummy(self, pk):
        (data, status_code), error = self.get_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = f"Error getting dummy {pk}"
            raise DummyError(msg)
        return data

    def create_dummy(self, name):
        (data, status_code), error = self.post_blocking("/dummy/", body={"name": name})
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.CREATED:
            msg = f"Error creating dummy {name}"
            raise DummyError(msg)
        return data

    def update_dummy(self, pk, name):
        (data, status_code), error = self.put_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}, body={"name": name}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.OK:
            msg = f"Error updating dummy {pk}"
            raise DummyError(msg)
        return data

    def delete_dummy(self, pk):
        (data, status_code), error = self.delete_blocking(
            "/dummy/{pk}/", path_params={"pk": pk}
        )
        if error:
            raise DummyError(error)
        if status_code != HTTPStatus.NO_CONTENT:
            msg = f"Error deleting dummy {pk}"
            raise DummyError(msg)
        return data
