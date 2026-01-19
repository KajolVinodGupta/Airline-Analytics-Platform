import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATION_API_KEY")
BASE_URL = "http://api.aviationstack.com/v1/flights"

def get_live_flights(limit=50):
    params = {
        "access_key": API_KEY,
        "limit": limit
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    records = []

    for flight in data.get("data", []):
        records.append({
            "flight_number": flight["flight"]["iata"],
            "airline": flight["airline"]["name"],
            "departure_airport": flight["departure"]["airport"],
            "arrival_airport": flight["arrival"]["airport"],
            "status": flight["flight_status"],
            "delay": flight["departure"]["delay"],
            "latitude": flight["live"]["latitude"] if flight.get("live") else None,
            "longitude": flight["live"]["longitude"] if flight.get("live") else None,
            "timestamp": flight["live"]["updated"] if flight.get("live") else None
        })

    return pd.DataFrame(records)
