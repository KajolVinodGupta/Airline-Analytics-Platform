import pandas as pd
from utils.upload_to_sql import get_engine, upload_dataframe

# Path to cleaned CSV
csv_path = "data/raw/flight_delay.csv"

print("Loading cleaned dataset...")
df = pd.read_csv(csv_path, low_memory=False)
print(f"Rows loaded: {len(df)}")

# Create SQL engine
engine = get_engine()

# Upload in chunks
chunk_size = 50000
total_rows = len(df)
print(f"Uploading to MySQL in chunks of {chunk_size} rows...")

for i in range(0, total_rows, chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    print(f"Uploading rows {i} to {i + len(chunk)}...")
    upload_dataframe(chunk, "flight_delay", engine, if_exists="append")

print("\n[SUCCESS] Full dataset uploaded to MySQL table: flight_delay")
