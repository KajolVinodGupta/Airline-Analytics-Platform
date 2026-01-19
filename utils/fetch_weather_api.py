import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHERSTACK_API_KEY")

# IATA → City mapping (extend anytime)
AIRPORT_CITY_MAP = {
    "JFK": "New York",
    "LAX": "Los Angeles",
    "SFO": "San Francisco",
    "ORD": "Chicago",
    "DEL": "Delhi",
    "BOM": "Mumbai",
    "DXB": "Dubai",
    "LHR": "London",
    "SIN": "Singapore",
}


def fetch_weather(iata_code: str):
    """Fetch live weather data from Weatherstack API."""

    iata_code = iata_code.upper()

    if iata_code not in AIRPORT_CITY_MAP:
        return None, f"❌ Airport code '{iata_code}' not found in mapping."

    city = AIRPORT_CITY_MAP[iata_code]

    url = (
        f"http://api.weatherstack.com/current?"
        f"access_key={API_KEY}&query={city}"
    )

    try:
        response = requests.get(url).json()
    except Exception as e:
        return None, f"❌ API request error: {e}"

    if "current" not in response:
        return None, f"❌ Weather data not found for {city}"

    return response["current"], None
