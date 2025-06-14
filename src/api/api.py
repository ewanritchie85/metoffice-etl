import os
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
from utils.utils import get_lat_long_from_city

# API key stored as an environment variable
# Make sure to create a .env file with the key METOFFICE_API_KEY
load_dotenv()
API_KEY = os.getenv("METOFFICE_API_KEY")

app = FastAPI()


@app.get("/health")
def health_check():
    """health check endpoint

    Returns:
        dict: A dictionary with the status of the API.
    """
    return {"status": "ok"}


@app.get("/sitespecific/v0/point/{span}")
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
