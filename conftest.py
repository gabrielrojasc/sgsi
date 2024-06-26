import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    return ["es_CL"]


# To make fixtures available to all test functions, add them here.
pytest_plugins = [
    "base.fixtures",
    "api_client.fixtures",
    "parameters.fixtures",
    "regions.fixtures",
    "users.fixtures",
    "documents.fixtures",
    "information_assets.fixtures",
    "risks.fixtures",
    "processes.fixtures",
]
