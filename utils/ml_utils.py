# utils/ml_utils.py
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

try:
    from prophet import Prophet
except Exception:
    Prophet = None


# ------------------------------------
# Utility: find a matching column name
# ------------------------------------
def find_col(df, candidates):
    for cand in candidates:
        if cand in df.columns:
            return cand
        # lowercase match
        for col in df.columns:
            if col.lower() == cand.lower():
                return col
    return None


# ============================================================
# TRAIN FLIGHT DELAY MODEL
# ============================================================
# ============================================================
# FIXED FINAL SCHEMA (same as Streamlit)
# ============================================================
CATEGORICAL = ["airline", "origin", "destination", "crs_dep_hour"]
NUMERIC = ["distance", "dep_delay", "taxi_out", "month", "dayofweek"]


# ============================================================
# CLEAN HOUR FROM CRSDepTime (HHMM)
# ============================================================
def extract_hour(value):
    try:
        v = int(float(value))
        return v // 100
    except:
        return np.nan


# ============================================================
# TRAIN FLIGHT DELAY MODEL — FINAL CONSISTENT VERSION
# ============================================================
def train_delay_model(
    df,
    sample_frac=0.1,
    save_path="models/flight_delay_model.pkl",
    random_state=42
):

    print("🔧 Training flight delay prediction model...")

    df = df.copy()

    # -------------------------------------
    # FIX: Clean + create consistent columns
    # -------------------------------------
    df["flight_date"] = pd.to_datetime(df["flight_date"], errors="coerce")

    df["airline"] = df["airline"].astype(str)
    df["origin"] = df["origin"].astype(str)
    df["destination"] = df["destination"].astype(str)

    df["arr_delay"] = pd.to_numeric(df["arr_delay"], errors="coerce")
    df["dep_delay"] = pd.to_numeric(df["dep_delay"], errors="coerce")
    df["distance"] = pd.to_numeric(df["distance"], errors="coerce")
    df["taxi_out"] = pd.to_numeric(df["taxi_out"], errors="coerce")

    # Hour extraction
    if "crs_dep_hour" not in df.columns:
        if "CRSDepTime" in df.columns:
            df["crs_dep_hour"] = df["CRSDepTime"].apply(extract_hour)
        else:
            df["crs_dep_hour"] = np.nan

    df["month"] = df["flight_date"].dt.month
    df["dayofweek"] = df["flight_date"].dt.weekday

    # Drop rows with no arrival delay (target missing)
    df = df.dropna(subset=["arr_delay"])
    df["is_delayed"] = (df["arr_delay"] > 15).astype(int)

    # Optional sampling
    if 0 < sample_frac < 1:
        df = df.sample(frac=sample_frac, random_state=random_state)

    # -------------------------------------
    # FIX: Use EXACT COLUMNS ALWAYS
    # -------------------------------------
    X = df[CATEGORICAL + NUMERIC].copy()
    y = df["is_delayed"]

    # Fill missing
    for col in CATEGORICAL:
        X[col] = X[col].fillna("UNK")
    for col in NUMERIC:
        X[col] = X[col].fillna(-1)

    # -------------------------------------
    # Preprocessor
    # -------------------------------------
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ("num", StandardScaler(), NUMERIC)
    ])

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=18,
        random_state=random_state,
        class_weight="balanced"
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])

    # Split + train
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    pipeline.fit(X_train, y_train)

    print("\n=== Classification Report ===")
    print(classification_report(y_test, pipeline.predict(X_test)))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, pipeline.predict(X_test)))

    # Save model
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, save_path)

    print(f"\n[SAVED] Model → {save_path}\n")


# ============================================================
# TRAIN PROPHET REVENUE FORECAST
# ============================================================
def train_revenue_prophet(df, save_path="models/revenue_forecast.pkl"):
    if Prophet is None:
        raise RuntimeError("Prophet is not installed.")

    df = df.copy()

    fd = find_col(df, ["flight_date", "FlightDate"])
    rv = find_col(df, ["revenue", "Revenue"])

    df["flight_date"] = pd.to_datetime(df[fd], errors="coerce")
    df["revenue"] = pd.to_numeric(df[rv], errors="coerce")

    df = df.dropna(subset=["flight_date", "revenue"])

    df_daily = (
        df.groupby("flight_date")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"flight_date": "ds", "revenue": "y"})
    )

    model = Prophet(yearly_seasonality=True)
    model.fit(df_daily)

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, save_path)

    print(f"[SAVED] Revenue Model → {save_path}")
