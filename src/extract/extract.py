from datetime import datetime
import json
import boto3
import logging
import os
from api.api import get_forecast_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_data_from_api(span: str, city: str) -> dict:
    """
    Get data from the API for a specific span and city.

    Args:
        span (str): The time span for the data - hourly / three-hourly / daily.
        city (str): The name of the city.

    Returns:
        dict: The JSON response from the API.
    """
    logger.info(f"fetching forecast data for {city} with span {span}")
    return get_forecast_data(span, city)


def upload_json_to_landing_s3(span: str, city: str, bucket=None, s3_client=None) -> str:
    """Uploads forecast data JSON to landing S3 bucket.

    Args:
        span (str): daily / hourly / three-hourly time span for the data.
        city (str): name of the city.
        bucket (str): name of the S3 bucket to upload to.
        s3_client (_type_, optional): Defaults to None, but is created if not provided.

    Returns:
        str: _description_
    """
    logger.info(f"uploading forecast data for {city} with span {span} to S3 bucket {bucket}")
    if not s3_client:
        s3_client = boto3.client("s3")
    if not bucket:
        bucket = os.getenv("LANDING_BUCKET_NAME")

    date = datetime.now()
    date_str = date.strftime("%Y/%m/%d/%H-%M")

    forecast_data = None
    try:
        forecast_data = get_data_from_api(span, city)
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Error fetching data from API: {e}")
        forecast_data = {"error": "Failed to fetch data from API"}

    s3_client.put_object(
        Bucket=bucket, Key=f"{city}/{date_str}.json", Body=json.dumps(forecast_data)
    )
    return f"{city}/{date_str}.json"
