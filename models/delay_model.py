import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier

# OPTIONAL (if installed)
try:
    from imblearn.over_sampling import RandomOverSampler
    IMB_AVAILABLE = True
except:
    IMB_AVAILABLE = False


def train_delay_model(df, sample_frac=0.05, enable_imbalance_fix=True):
    print("Original Dataset Size:", len(df))

    # -----------------------------
    # 1. SAMPLE FOR TRAINING  
    # -----------------------------
    if sample_frac < 1.0:
        df = df.sample(frac=sample_frac, random_state=42)
        print(f"Sampled dataset (frac={sample_frac}):", len(df))

    # -----------------------------
    # 2. FEATURE ENGINEERING
    # -----------------------------
    df["hour"] = pd.to_datetime(df["flight_date"]).dt.hour

    X = df[["seats_sold", "ticket_price", "hour"]]
    y = df["delayed"]  # Ensure you created this column earlier

    # -----------------------------
    # 3. TRAIN / TEST SPLIT
    # -----------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # -----------------------------
    # 4. HANDLE IMBALANCED CLASSES
    # -----------------------------
    if enable_imbalance_fix and IMB_AVAILABLE:
        ros = RandomOverSampler()
        X_train, y_train = ros.fit_resample(X_train, y_train)
        print("Oversampling applied. New train size:", len(X_train))
    else:
        print("Using class_weight='balanced' ")

    # -----------------------------
    # 5. TRAIN MODEL
    # -----------------------------
    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        class_weight="balanced" if not IMB_AVAILABLE else None,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # -----------------------------
    # 6. EVALUATION
    # -----------------------------
    y_pred = model.predict(X_test)
    print("\n===== CLASSIFICATION REPORT =====\n")
    print(classification_report(y_test, y_pred))

    return model
