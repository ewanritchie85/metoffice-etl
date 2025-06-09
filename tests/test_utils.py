import os
from unittest.mock import patch, MagicMock
import logging
import pytest
from utils.utils import (
    setup_logger,
    get_s3_client_and_landing_bucket,
    get_lat_long_from_city,
)


class TestGetLatLong:
    def test_get_lat_long_from_real_city(self):
        test_city = "Tokyo"
        expected_lat_long = (35.6870, 139.7495)
        lat_long = get_lat_long_from_city(test_city)
        assert lat_long == expected_lat_long

    def test_get_lat_long_from_non_existent_city(self):
        test_city = "NonExistentCity"
        with pytest.raises(ValueError) as e:
            get_lat_long_from_city(test_city)
        assert str(e.value) == "'NonExistentCity' not found in the dataset."

    def test_get_lat_long_from_city_with_extra_spaces(self):
        test_city = "  London  "
        expected_lat_long = (51.5072, -0.1275)
        lat_long = get_lat_long_from_city(test_city)
        assert lat_long == expected_lat_long

    def test_get_lat_long_from_non_ascii_city_(self):
        test_city = "São Paulo"
        expected_lat_long = (-23.5504, -46.6339)
        lat_long = get_lat_long_from_city(test_city)
        assert lat_long == expected_lat_long


class TestSetupLogger:
    def test_returns_logger_instance(self):
        logger = setup_logger("test_logger")
        assert isinstance(logger, logging.Logger)

    def test_logs_info_message(self, caplog):
        logger = setup_logger("test_logger2")
        with caplog.at_level(logging.INFO):
            logger.info("Test log message")
        assert "Test log message" in caplog.text


class TestGetS3ClientAndLandingBucket:
    @patch("boto3.client")
    def test_returns_client_and_env_bucket(self, mock_boto):
        mock_client = MagicMock()
        mock_boto.return_value = mock_client
        os.environ["LANDING_BUCKET_NAME"] = "test-bucket"
        client, bucket = get_s3_client_and_landing_bucket()
        assert client == mock_client
        assert bucket == "test-bucket"

    @patch("boto3.client")
    def test_returns_client_and_provided_bucket(self, mock_boto):
        mock_client = MagicMock()
        mock_boto.return_value = mock_client
        client, bucket = get_s3_client_and_landing_bucket(bucket="manual-bucket")
        assert client == mock_client
        assert bucket == "manual-bucket"

    def test_returns_provided_client_and_env_bucket(self):
        mock_client = MagicMock()
        os.environ["LANDING_BUCKET_NAME"] = "test-bucket-2"
        client, bucket = get_s3_client_and_landing_bucket(s3_client=mock_client)
        assert client == mock_client
        assert bucket == "test-bucket-2"

    def test_returns_provided_client_and_bucket(self):
        mock_client = MagicMock()
        client, bucket = get_s3_client_and_landing_bucket(
            s3_client=mock_client, bucket="explicit-bucket"
        )
        assert client == mock_client
        assert bucket == "explicit-bucket"
