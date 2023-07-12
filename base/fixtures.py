from typing import TYPE_CHECKING

import pytest

from base.middleware import RequestMiddleware

if TYPE_CHECKING:
    from django.test.client import Client


# If you defined fixtures for a model, but they use a non-standard name, please
# add them to the following mapping. Keys follow the `app_label.model_name` scheme.
MODEL_FIXTURE_CUSTOM_NAMES = {
    "users.User": "regular_user",
    "parameters.Parameter": "test_parameter",
}


@pytest.fixture
def superuser_client(db, superuser_user) -> "Client":
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(superuser_user)
    yield client
    if hasattr(RequestMiddleware.thread_local, "user"):
        del RequestMiddleware.thread_local.user


@pytest.fixture
def staff_client(db, staff_user) -> "Client":
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(staff_user)
    yield client
    if hasattr(RequestMiddleware.thread_local, "user"):
        del RequestMiddleware.thread_local.user


@pytest.fixture
def regular_user_client(db, regular_user) -> "Client":
    """A Django test client logged in as an admin user."""
    from django.test.client import Client

    client = Client()
    client.force_login(regular_user)
    yield client
    if hasattr(RequestMiddleware.thread_local, "user"):
        del RequestMiddleware.thread_local.user