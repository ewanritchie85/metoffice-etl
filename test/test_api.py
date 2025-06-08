from fastapi.testclient import TestClient
import pytest
from api.api import app
from utils.utils import get_lat_long_from_city


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_response(client):
    test_city = "Tokyo"
    test_span = "daily"
    test_response = client.get(
        f"/sitespecific/v0/point/{test_span}?city={test_city}",
    )
    return test_response


class TestHealthCheck:
    def test_api_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        assert response.headers["Content-Type"] == "application/json"


class TestGetHourlyData:
    def test_get_hourly_data(self, test_response):

        assert test_response.status_code == 200
        assert test_response.headers["Content-Type"] == "application/json"
        assert "features" in test_response.json()
