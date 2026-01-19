import pandas as pd
import numpy as np


# ============================================================
# 1) CLEAN FLIGHT DELAY DATA
# ============================================================
def clean_flight_delay_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the merged flight delay dataset.
    - Ensures correct datetime formats
    - Handles missing delays
    - Converts identifier columns to string
    - Drops rows with impossible values
    """

    df = df.copy()

    # ----------------------------
    # Ensure correct data types
    # ----------------------------
    string_cols = [
        "airline", "origin", "destination", "airport_name",
        "origin_city", "origin_state", "country", "dest_city", "dest_state"
    ]

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)

    # Date column already exists from step 3 script
    df["flight_date"] = pd.to_datetime(df["flight_date"], errors="coerce")

    # Remove rows with invalid dates
    df = df[df["flight_date"].notna()]

    # -------------------------------------------------
    # Handle missing delays — replace NA with zero
    # -------------------------------------------------
    delay_columns = [
        "dep_delay", "arr_delay", "air_system_delay", "security_delay",
        "airline_delay", "late_aircraft_delay", "weather_delay"
    ]

    for col in delay_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # -------------------------------------------------
    # Ensure numeric columns are numeric
    # -------------------------------------------------
    numeric_cols = [
        "distance", "scheduled_time", "elapsed_time", "air_time",
        "taxi_out", "taxi_in"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # -------------------------------------------------
    # Remove rows with impossible distances (< 10 miles)
    # -------------------------------------------------
    df = df[df["distance"] >= 10]

    return df


# ============================================================
# 2) CLEAN SALES DATA
# ============================================================
def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans sales dataset:
    - Ensures date format
    - Converts revenue, passengers to numeric
    - Removes rows with missing route or airline
    """

    df = df.copy()

    # Ensure date format
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Drop rows with invalid dates
    df = df[df["date"].notna()]

    # Convert numeric fields
    numeric_cols = ["tickets_sold", "avg_ticket_price", "revenue"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Ensure airline and route are string
    df["airline"] = df["airline"].astype(str)
    df["route"] = df["route"].astype(str)

    # Remove rows where airline or route is missing
    df = df[(df["airline"] != "nan") & (df["route"] != "nan")]

    # Filter out negative values (bad data)
    df = df[df["revenue"] >= 0]
    df = df[df["tickets_sold"] >= 0]

    return df


# ============================================================
# 3) EXPORTER
# ============================================================
def save_cleaned(df: pd.DataFrame, output_path: str):
    """
    Saves a cleaned dataframe safely.
    """
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved cleaned file → {output_path}")
    print(f"Rows: {len(df)}")
