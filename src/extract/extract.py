from datetime import datetime
import json
import dotenv
from api.api import get_forecast_data
from utils.utils import get_s3_client_and_landing_bucket, setup_logger

logger = setup_logger(__name__)

dotenv.load_dotenv()


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
    return get_forecast_data(city, span)


def upload_json_to_landing_s3(span: str, city: str, bucket=None, s3_client=None) -> str:
    """Uploads forecast data JSON to landing S3 bucket.

    Args:
        span (str): daily / hourly / three-hourly time span for the data.
        city (str): name of the city.
        bucket (str): name of the S3 bucket to upload to.
        s3_client: Defaults to None, but is created if not provided.

    Returns:
        str: path to S3 object. just for reference and verification
    """
    logger.info(f"Initialising s3 client")
    s3_client, bucket = get_s3_client_and_landing_bucket(bucket, s3_client)
    logger.info(
        f"uploading forecast data for {city} with span {span} to S3 bucket {bucket}"
    )

    date = datetime.now()
    date_str = date.strftime("%Y/%m/%d/%H")

    forecast_data = None
    try:
        forecast_data = get_data_from_api(span, city)
    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Error fetching data from API: {e}")
        forecast_data = {"error": "Failed to fetch data from API"}

    s3_client.put_object(
        Bucket=bucket, Key=f"{date_str}/{city}.json", Body=json.dumps(forecast_data)
    )
    return f"{date_str}/{city}.json"


# temporary main function to test extraction and upload
if __name__ == "__main__":
    upload_json_to_landing_s3("daily", "London")
