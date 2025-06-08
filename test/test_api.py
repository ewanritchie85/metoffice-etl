from fastapi.testclient import TestClient
import pytest
from api.api import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_response(client):
    test_latitude = 57.149651
    test_longitude = -2.099075
    test_response = client.get(
        f"/sitespecific/v0/point/hourly?latitude={test_latitude}&longitude={test_longitude}"
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
