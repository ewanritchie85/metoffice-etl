from unittest.mock import patch
import pytest


@pytest.fixture
def mock_data():
    return {"features": [{"type": "Feature", "properties": {"key": "value"}}]}


class TestGetForecastData:
    def test_get_forecast_data(self, mock_data):

        with patch("api.api.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_data

            from api.api import get_forecast_data

            result = get_forecast_data("Tokyo")

            assert "features" in result
