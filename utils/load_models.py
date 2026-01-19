# utils/load_models.py
import joblib
from pathlib import Path

MODEL_DIR = Path("models")

def load_delay_model(path=None):
    if path is None:
        path = MODEL_DIR / "flight_delay_model.pkl"
    else:
        path = Path(path)
    if not path.exists():
        print(f"⚠️ Delay model not found at: {path}")
        return None
    return joblib.load(path)


def load_revenue_model(path=None):
    if path is None:
        path = MODEL_DIR / "revenue_forecast.pkl"
    else:
        path = Path(path)
    if not path.exists():
        print(f"⚠️ Revenue model not found at: {path}")
        return None
    return joblib.load(path)
