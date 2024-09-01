import pytest
from falcon.testing import TestClient as FalconTestClient

from src.app import create_app


@pytest.fixture(scope="function")
def client() -> FalconTestClient:
    return FalconTestClient(create_app())
