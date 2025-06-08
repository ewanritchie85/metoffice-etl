from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest
from api.api import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_data():
    mock_data = {"features": [{"type": "Feature", "properties": {"key": "value"}}]}
    return mock_data


class TestHealthCheck:
    def test_api_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        assert response.headers["Content-Type"] == "application/json"


class TestGetHourlyData:
    def test_get_hourly_data(self, client, mock_data):

        with patch("api.api.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_data
            mock_get.return_value.headers = {"Content-Type": "application/json"}

            response = client.get("/sitespecific/v0/point/daily?city=Tokyo")

            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
            assert "features" in response.json()
