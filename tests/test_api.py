from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest


@pytest.fixture
def mock_data():
    mock_data = {"features": [{"type": "Feature", "properties": {"key": "value"}}]}
    return mock_data


class TestGetHourlyData:
    def test_get_forecast_data(self, client, mock_data):

        with patch("api.api.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_data
            mock_get.return_value.headers = {"Content-Type": "application/json"}

            response = client.get("/sitespecific/v0/point/daily?city=Tokyo")

            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
            assert "features" in response.json()
