from api.api import get_forecast_data


def get_data_from_api(span: str, city: str) -> dict:
    """
    Get data from the API for a specific span and city.

    Args:
        span (str): The time span for the data - hourly / three-hourly / daily.
        city (str): The name of the city.

    Returns:
        dict: The JSON response from the API.
    """
    print("getting_data_from_api called")
    return get_forecast_data(span, city)

def upload_json_to_landing_s3() -> None:
    """
    Upload the JSON data to the landing S3 bucket.
    This function is a placeholder and should be implemented.
    """
    print("upload_json_to_landing_s3 called")
    # Implementation goes here
    pass