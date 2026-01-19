from utils.run_query import run_query
from utils.ml_utils import train_delay_model, train_revenue_prophet

def main():
    print("📥 Loading data from MySQL...")

    flight_df = run_query("SELECT * FROM flight_delay")
    sales_df  = run_query("SELECT * FROM sales_data")

    print("Flight rows:", len(flight_df))
    print("Sales rows:", len(sales_df))

    # -------------------------------
    # Train Delay Model
    # -------------------------------
    train_delay_model(
        flight_df,
        save_path="models/flight_delay_model.pkl",
        sample_frac=0.10
    )

    # -------------------------------
    # Train Revenue Prophet (optional)
    # -------------------------------
    if len(sales_df) > 0:
        try:
            train_revenue_prophet(
                sales_df,
                save_path="models/revenue_forecast.pkl"
            )
        except Exception as e:
            print("Prophet training failed:", e)
    else:
        print("⚠️ No sales_data rows — skipping Prophet.")


if __name__ == "__main__":
    main()
