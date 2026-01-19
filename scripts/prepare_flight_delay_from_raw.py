# scripts/prepare_flight_delay_from_raw.py
import os
import pandas as pd
from datetime import datetime

# CONFIG
FLIGHT_CSV = "data/raw/flight.csv"
AIRLINE_CSV = "data/raw/airline.csv"   # has IATA_CODE, AIRLINE
AIRPORT_CSV = "data/raw/airport.csv"   # has IATA_CODE, AIRPORT, CITY, STATE, COUNTRY, LATITUDE, LONGITUDE
OUT_PATH = "data/raw/flight_delay.csv"

# Read CSVs robustly (prevent dtype warnings / memory issues)
print("Loading CSVs (this may take a while for large files)...")
flights = pd.read_csv(FLIGHT_CSV, dtype=str, low_memory=False)
airlines = pd.read_csv(AIRLINE_CSV, dtype=str, low_memory=False)
airports = pd.read_csv(AIRPORT_CSV, dtype=str, low_memory=False)

print(f"Loaded flights: {len(flights)} rows")
print(f"Loaded airlines: {len(airlines)} rows")
print(f"Loaded airports: {len(airports)} rows")

# Standardize column names (strip)
flights.columns = flights.columns.str.strip()
airlines.columns = airlines.columns.str.strip()
airports.columns = airports.columns.str.strip()

# Convert YEAR/MONTH/DAY to numeric then to date
for c in ["YEAR", "MONTH", "DAY"]:
    if c in flights.columns:
        flights[c] = pd.to_numeric(flights[c], errors="coerce").astype("Int64")

def make_flight_date(df):
    if {"YEAR", "MONTH", "DAY"}.issubset(df.columns):
        # create date, coerce invalid to NaT
        return pd.to_datetime(df.loc[:, ["YEAR", "MONTH", "DAY"]], errors="coerce")
    # fallback to any date-like column
    for col in ["FLIGHT_DATE", "DATE", "SCHEDULED_DEPARTURE_DATE"]:
        if col in df.columns:
            return pd.to_datetime(df[col], errors="coerce")
    return pd.NaT

flights["flight_date"] = make_flight_date(flights)

# Numeric columns to convert (delays, distance, times)
num_cols = [
    "DEPARTURE_DELAY","ARRIVAL_DELAY","TAXI_OUT","TAXI_IN",
    "DISTANCE","SCHEDULED_DEPARTURE","DEPARTURE_TIME","WHEELS_OFF",
    "SCHEDULED_ARRIVAL","ARRIVAL_TIME","ELAPSED_TIME","AIR_TIME",
    "AIR_SYSTEM_DELAY","SECURITY_DELAY","AIRLINE_DELAY","LATE_AIRCRAFT_DELAY","WEATHER_DELAY"
]
for col in num_cols:
    if col in flights.columns:
        flights[col] = pd.to_numeric(flights[col], errors="coerce")

# Standardize key columns (uppercase, strip)
if "ORIGIN_AIRPORT" in flights.columns:
    flights["origin"] = flights["ORIGIN_AIRPORT"].astype(str).str.strip()
else:
    flights["origin"] = None

if "DESTINATION_AIRPORT" in flights.columns:
    flights["destination"] = flights["DESTINATION_AIRPORT"].astype(str).str.strip()
else:
    flights["destination"] = None

# Flight number
if "FLIGHT_NUMBER" in flights.columns:
    flights["flight_number"] = flights["FLIGHT_NUMBER"].astype(str).str.strip()
else:
    flights["flight_number"] = None

# Cancelled / Diverted flags
for f in ["CANCELLED", "DIVERTED"]:
    if f in flights.columns:
        flights[f] = pd.to_numeric(flights[f], errors="coerce").fillna(0).astype("Int64")
    else:
        flights[f] = 0

# Map airline code (IATA) to airline name using airlines CSV
# flight file has column AIRLINE (IATA code) — ensure uppercase & stripped
if "AIRLINE" in flights.columns:
    flights["AIRLINE_CODE"] = flights["AIRLINE"].astype(str).str.strip()
else:
    flights["AIRLINE_CODE"] = None

airlines = airlines.rename(columns={c: c.strip() for c in airlines.columns})
# find likely airline name column (common names: AIRLINE, Name)
airline_name_col = None
for cand in ["AIRLINE","Airline","NAME","Name","airline"]:
    if cand in airlines.columns:
        airline_name_col = cand
        break

if airline_name_col is None and len(airlines.columns) >= 2:
    # assume second column is name
    airline_name_col = airlines.columns[1]

airlines_lookup = airlines[["IATA_CODE", airline_name_col]].rename(
    columns={"IATA_CODE":"AIRLINE_CODE", airline_name_col:"airline_name"}
)

flights = flights.merge(airlines_lookup, on="AIRLINE_CODE", how="left")

# Enrich origin/destination with airport city names (if available)
airports = airports.rename(columns={c: c.strip() for c in airports.columns})
airport_lookup = airports[["IATA_CODE","AIRPORT","CITY","STATE","COUNTRY","LATITUDE","LONGITUDE"]].rename(
    columns={"IATA_CODE":"iata","AIRPORT":"airport_name","CITY":"city","STATE":"state","COUNTRY":"country","LATITUDE":"lat","LONGITUDE":"lon"}
)

# left join to get origin city
flights = flights.merge(airport_lookup, left_on="origin", right_on="iata", how="left", suffixes=("","_origin"))
# rename origin fields
if "airport_name" in flights.columns:
    flights = flights.rename(columns={"airport_name":"origin_airport_name","city":"origin_city","state":"origin_state","country":"origin_country","lat":"origin_lat","lon":"origin_lon"})
# merge destination (we must avoid overwriting columns from previous merge)
airport_lookup_dest = airport_lookup.add_suffix("_dest")
flights = flights.merge(airport_lookup_dest, left_on="destination", right_on="iata_dest", how="left")

# Now build the columns matching flight_history schema:
# target: flight_date, airline, flight_number, origin, destination, dep_delay, arr_delay, distance, cancelled

out = pd.DataFrame()
out["flight_date"] = flights["flight_date"]
# prefer airline name, fallback to code
out["airline"] = flights.get("airline_name").fillna(flights.get("AIRLINE_CODE"))
out["flight_number"] = flights.get("flight_number")
out["origin"] = flights.get("origin")
out["destination"] = flights.get("destination")
out["dep_delay"] = flights.get("DEPARTURE_DELAY")
out["arr_delay"] = flights.get("ARRIVAL_DELAY")
out["distance"] = flights.get("DISTANCE")
out["cancelled"] = flights.get("CANCELLED").fillna(0).astype("Int64")
# optional additional columns for analysis
out["diverted"] = flights.get("DIVERTED").fillna(0).astype("Int64")
out["air_system_delay"] = flights.get("AIR_SYSTEM_DELAY")
out["security_delay"] = flights.get("SECURITY_DELAY")
out["airline_delay"] = flights.get("AIRLINE_DELAY")
out["late_aircraft_delay"] = flights.get("LATE_AIRCRAFT_DELAY")
out["weather_delay"] = flights.get("WEATHER_DELAY")

# Flag rows with missing essential values
out["_missing_dep_delay"] = out["dep_delay"].isna()
out["_missing_arr_delay"] = out["arr_delay"].isna()
out["_missing_date"] = out["flight_date"].isna()

# Clean: convert flight_date to dateonly (no time)
out["flight_date"] = pd.to_datetime(out["flight_date"], errors="coerce").dt.date

# Save file (CSV)
os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
out.to_csv(OUT_PATH, index=False)
print(f"[SUCCESS] Wrote cleaned flight_delay file to: {OUT_PATH}")
print("Rows:", len(out))
print("Missing dep_delay:", out['_missing_dep_delay'].sum())
print("Missing arr_delay:", out['_missing_arr_delay'].sum())
print("Missing flight_date:", out['_missing_date'].sum())
