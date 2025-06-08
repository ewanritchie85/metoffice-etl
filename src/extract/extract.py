from api.api import get_forecast_data


def get_data_from_api(span: str, city: str):
    """
    Get data from the API for a specific span and city.

    Args:
        span (str): The time span for the data - houryl / three-hourly / daily.
        city (str): The name of the city.

    Returns:
        dict: The JSON response from the API.
    """
    return get_forecast_data(span, city)
