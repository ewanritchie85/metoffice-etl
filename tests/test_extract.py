from unittest.mock import patch, MagicMock
import pytest
import json
from src.extract.extract import upload_json_to_landing_s3, get_data_from_api


@pytest.fixture
def mock_s3_resources():
    mock_s3 = MagicMock()
    mock_bucket = "test_bucket"
    return mock_s3, mock_bucket


class TestExtractFunction:
    def test_get_data_from_api(self):
        test_span = "daily"
        test_city = "Tokyo"
        result = get_data_from_api(test_span, test_city)

        assert isinstance(result, dict)
        assert "features" in result
        assert result["features"][0]["type"] == "Feature"

    @patch("src.extract.extract.get_s3_client_and_landing_bucket")
    @patch("src.extract.extract.get_data_from_api")
    def test_upload_json_to_s3(
        self, mock_get_data, mock_get_s3_client_and_bucket, mock_s3_resources
    ):
        mock_s3, mock_bucket = mock_s3_resources
        mock_get_s3_client_and_bucket.return_value = (mock_s3, mock_bucket)
        mock_get_data.return_value = {"features": []}

        result = upload_json_to_landing_s3("daily", "London")

        assert result.endswith("London.json")
        mock_s3.put_object.assert_called_once()

    @patch("src.extract.extract.get_s3_client_and_landing_bucket")
    @patch(
        "src.extract.extract.get_data_from_api",
        side_effect=ConnectionError("API unreachable"),
    )
    def test_upload_json_to_s3_connection_error(
        self, mock_get_data, mock_get_s3_client_and_bucket, mock_s3_resources
    ):
        mock_s3, mock_bucket = mock_s3_resources
        mock_get_s3_client_and_bucket.return_value = (mock_s3, mock_bucket)

        upload_json_to_landing_s3("daily", "London")
        args, kwargs = mock_s3.put_object.call_args
        body = json.loads(kwargs["Body"])
        assert body == {"error": "Failed to fetch data from API"}
