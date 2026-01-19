import pandas as pd
from datetime import datetime
from delay_model import train_delay_model

df = pd.read_csv("data/flight_delay.csv")

print("Training delay model...")

model = train_delay_model(
    df,
    sample_frac=0.05,    # use 5% of data
    enable_imbalance_fix=True
)

# -----------------------------
# SAVE REPORT LOGS
# -----------------------------
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")

with open(f"reports/delay_report_{timestamp}.txt", "w") as f:
    import sys
    sys.stdout = f  # redirect prints to file
    train_delay_model(df)
    sys.stdout = sys.__stdout__

print("Report saved in /reports/")
