import pytest
from requests import request, ConnectionError

from tests.constants import BASE_URL


@pytest.fixture(autouse=True)
def chk_service_runs():
    url = f"{BASE_URL}/health"
    try:
        response = request("GET", url)
    except ConnectionError as e:
        pytest.fail(f"API service is not running: {e}")
