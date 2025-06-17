import os
from dotenv import load_dotenv
import requests
from utils.utils import get_lat_long_from_city


if os.getenv("RUNNING_IN_ECS") != "true":
    load_dotenv()
API_KEY = os.getenv("METOFFICE_API_KEY")


def get_forecast_data(city: str, span: str = "daily"):
    lat_long = get_lat_long_from_city(city)
    latitude, longitude = lat_long[0], lat_long[1]
    url = f"https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/{span}"
    headers = {"accept": "application/json", "apikey": API_KEY}
    params = {
        "latitude": latitude,
        "longitude": longitude,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
