from unittest.mock import patch, MagicMock
from src.extract.extract import upload_json_to_landing_s3


from src.extract.extract import get_data_from_api


class TestExtractFunction:
    def test_get_data_from_api(self):
        test_span = "daily"
        test_city = "Tokyo"
        result = get_data_from_api(test_span, test_city)

        assert isinstance(result, dict)
        assert "features" in result
        assert result["features"][0]["type"] == "Feature"

    @patch("src.extract.extract.get_data_from_api")
    @patch("src.extract.extract.get_s3_client_and_landing_bucket")
    def test_upload_json_to_s3(self, mock_get_client_and_bucket, mock_get_data):
        mock_s3 = MagicMock()
        mock_bucket = "test_bucket"
        mock_get_client_and_bucket.return_value = (mock_s3, mock_bucket)
        mock_get_data.return_value = {"features": []}

        result = upload_json_to_landing_s3("daily", "London")

        assert result.endswith(".json")
        mock_s3.put_object.assert_called_once()
