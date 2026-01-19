import pandas as pd
from utils.upload_to_sql import get_engine, upload_dataframe

engine = get_engine()

# ------- Upload Airlines -------
df_airlines = pd.read_csv("data/raw/airline.csv")
upload_dataframe(df_airlines, "airlines", engine, if_exists="replace")

# ------- Upload Airports -------
df_airports = pd.read_csv("data/raw/airport.csv")
upload_dataframe(df_airports, "airports", engine, if_exists="replace")

print("Upload complete: airlines + airports tables.")
