import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock
from src.transform.transform import transform_data_to_dataframe


@pytest.fixture
def sample_json():
    return {
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-0.1, 51.5, 15.0]},
                "properties": {
                    "timeSeries": [
                        {
                            "time": "2025-06-08T00:00Z",
                            "midday10MWindSpeed": 5.76,
                            "nightProbabilityOfRain": 5,
                        }
                    ]
                },
            }
        ]
    }


@patch("src.transform.transform.get_s3_client_and_landing_bucket")
def test_transform_data_to_dataframe(mock_get_s3, sample_json):
    mock_s3 = MagicMock()
    mock_bucket = "test-bucket"
    mock_key = "London.json"
    mock_get_s3.return_value = (mock_s3, mock_bucket)

    mock_s3.list_objects_v2.return_value = {"Contents": [{"Key": mock_key}]}

    mock_body = MagicMock()
    mock_body.read.return_value = json.dumps(sample_json).encode("utf-8")
    mock_s3.get_object.return_value = {"Body": mock_body}

    result = transform_data_to_dataframe()

    # Check if result is list of DataFrames
    assert isinstance(result, list)
    assert all(isinstance(df, pd.DataFrame) for df in result)
