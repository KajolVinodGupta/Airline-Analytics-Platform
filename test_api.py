from utils.fetch_flight_api import get_live_flights

df = get_live_flights()
print(df.head())
print("Rows fetched:", len(df))
