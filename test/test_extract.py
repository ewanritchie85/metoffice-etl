from unittest.mock import patch
import pytest


from src.extract.extract import get_data_from_api


@pytest.fixture(autouse=True)
def mock_api_response():
    with patch("src.extract.extract.get_data_from_api") as mock_func:
        mock_func.return_value = {
            "features": [{"type": "Feature", "properties": {"key": "value"}}]
        }
        return mock_func


class TestExtractFunction:
    def test_get_data_from_api(self):
        test_span = "daily"
        test_city = "Tokyo"
        result = get_data_from_api(test_span, test_city)

        assert isinstance(result, dict)
        assert "features" in result
        assert result["features"][0]["type"] == "Feature"