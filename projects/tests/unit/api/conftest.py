import pytest
from starlette.testclient import TestClient

from orbify_projects.core.config import settings
from orbify_projects.main import app


@pytest.fixture(scope="session")
def endpoint_uri():
    def wrapped(endpoint: str) -> str:
        return f"{settings.api_prefix}/{endpoint}"

    return wrapped


@pytest.fixture(scope="session")
def client(db_session):
    with TestClient(app) as test_client:
        yield test_client
