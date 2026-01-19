import pandas as pd
import os

# Configurable defaults
DEFAULT_SEATS_SOLD = 100
DEFAULT_TICKET_PRICE = 200
DEFAULT_CLASS = "Economy"

# Load CSVs with safe dtype handling
flight_csv = "data/raw/flight.csv"
airline_csv = "data/raw/airline.csv"
airport_csv = "data/raw/airport.csv"

# Force all columns to string to avoid mixed dtype issues
flights = pd.read_csv(flight_csv, dtype=str, low_memory=False)
airlines = pd.read_csv(airline_csv, dtype=str)
airports = pd.read_csv(airport_csv, dtype=str)

# Convert numeric columns where required
numeric_cols = ["FLIGHT_NUMBER", "YEAR", "MONTH", "DAY"]
for col in numeric_cols:
    flights[col] = pd.to_numeric(flights[col], errors="coerce")

# Merge airline names
flights = flights.merge(
    airlines,
    left_on="AIRLINE",
    right_on="IATA_CODE",
    how="left"
)

# airline name column
flights["airline"] = flights["AIRLINE_y"]

# Convert flight_date safely
flights["flight_date"] = pd.to_datetime(
    flights[["YEAR", "MONTH", "DAY"]],
    errors="coerce"
)

# origin & destination: ensure string
flights["origin"] = flights["ORIGIN_AIRPORT"].astype(str).str.strip()
flights["destination"] = flights["DESTINATION_AIRPORT"].astype(str).str.strip()

# Create route safely
flights["route"] = flights["origin"].fillna("") + "-" + flights["destination"].fillna("")

# Flight number clean
flights["flight_number"] = flights["FLIGHT_NUMBER"].astype("Int64")

# Default values
flights["seats_sold"] = DEFAULT_SEATS_SOLD
flights["ticket_price"] = DEFAULT_TICKET_PRICE
flights["class"] = DEFAULT_CLASS
flights["revenue"] = flights["seats_sold"] * flights["ticket_price"]

# Final dataset
sales_data = flights[[
    "flight_date",
    "airline",
    "flight_number",
    "origin",
    "destination",
    "route",
    "seats_sold",
    "ticket_price",
    "revenue",
    "class"
]]

# Save result
os.makedirs("data/raw", exist_ok=True)
sales_data.to_csv("data/raw/sales_data.csv", index=False)

print(f"[SUCCESS] Saved sales_data.csv with {len(sales_data)} rows")
