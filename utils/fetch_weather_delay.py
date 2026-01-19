import requests
import pandas as pd

API = "https://aviationweather.gov/api/data/metar?ids={}"

def get_airport_weather(iata):
    url = API.format(iata)
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None

        return r.text
    except:
        return None
