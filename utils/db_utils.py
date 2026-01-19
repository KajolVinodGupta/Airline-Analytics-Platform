import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import os

def get_engine():
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_NAME = os.getenv("DB_NAME", "airline_db")

    return create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")

def load_flight_history():
    engine = get_engine()
    return pd.read_sql("SELECT * FROM flight_delay", engine)

def load_sales_data():
    engine = get_engine()
    return pd.read_sql("SELECT * FROM sales_data", engine)
