# utils/data_utils.py
import os
import pandas as pd
from io import StringIO

DEMO_PATH = os.path.join("data", "demo_flight_data.csv")

def _ensure_data_folder():
    os.makedirs("data", exist_ok=True)

def get_default_demo_csv():
    """
    Small demo dataset with the columns your app expects.
    """
    csv = """flight_date,airline,flight_number,origin,destination,route,seats_sold,ticket_price,revenue,arr_delay,travel_class
2025-01-01,Air India,AI101,DEL,BOM,DEL-BOM,120,4500,540000,10,Economy
2025-01-02,IndiGo,6E202,BOM,DEL,BOM-DEL,150,4200,630000,5,Economy
2025-01-03,SpiceJet,SG303,BLR,HYD,BLR-HYD,90,3800,342000,25,Business
2025-01-04,Vistara,UK404,DEL,BLR,DEL-BLR,110,5000,550000,35,Economy
2025-01-05,Air India,AI505,HYD,DEL,HYD-DEL,130,4700,611000,0,Economy
"""
    return csv

def write_demo_csv(path=DEMO_PATH):
    _ensure_data_folder()
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(get_default_demo_csv())
    return path

def load_demo_data(path=DEMO_PATH):
    """
    Loads demo CSV from data/demo_flight_data.csv.
    If file missing, it will create one using default demo content.
    """
    _ensure_data_folder()
    if not os.path.exists(path):
        write_demo_csv(path)
    try:
        df = pd.read_csv(path, parse_dates=["flight_date"])
        return df
    except Exception as e:
        print(f"Error loading demo dataset: {e}")
        return None

def load_csv_file(uploaded_file):
    """
    uploaded_file can be a Streamlit UploadedFile or a path.
    """
    if uploaded_file is None:
        return None
    try:
        # if it's a file-like object (Streamlit), pandas can read it directly
        df = pd.read_csv(uploaded_file, parse_dates=["flight_date"], infer_datetime_format=True)
    except Exception:
        # fallback: read without date parsing
        df = pd.read_csv(uploaded_file)
    return df
