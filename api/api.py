from fastapi import FastAPI
from dotenv import load_dotenv
from pprint import pprint
import os
import requests

load_dotenv()
API_KEY = os.getenv("METOFFICE_API_KEY")

app = FastAPI()


@app.get("/health")
async def health_check():
    """health check endpoint

    Returns:
        dict: A dictionary with the status of the API.
    """
    return {"status": "ok"}


@app.get("/sitespecific/v0/point/hourly")
async def get_hourly_data(latitude: float, longitude: float):

    url = "https://data.hub.api.metoffice.gov.uk/sitespecific/v0/point/hourly"
    headers = {"accept": "application/json", "apikey": API_KEY}
    params = {
        "latitude": latitude,
        "longitude": longitude,
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    
    pprint(response.json())
    return response.json()
