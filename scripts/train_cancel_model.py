import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

print("⚡ Starting script...")

try:
    df = pd.read_csv("data/raw/flight.csv")
    print("📄 CSV loaded successfully!")
except Exception as e:
    print("❌ CSV load error:", e)
    exit()

print("🔍 Selecting required columns...")

try:
    df = df[[
        "Airline", "Origin", "Dest",
        "DepDelayMinutes", "Distance",
        "Month", "DayOfWeek",
        "Cancelled"
    ]]
    print("✅ Column selection OK")
except Exception as e:
    print("❌ Column selection failed:", e)
    exit()

df = df.dropna()
print("🧹 Missing rows dropped. Remaining rows:", len(df))

encoders = {}
for col in ["Airline", "Origin", "Dest"]:
    print(f"🔠 Encoding column: {col}")
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df.drop("Cancelled", axis=1)
y = df["Cancelled"]

print("📊 Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("🤖 Training model...")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)

print("💾 Saving model bundle...")
bundle = {
    "model": model,
    "encoders": encoders,
    "features": list(X.columns)
}

try:
    pickle.dump(bundle, open("models/cancellation_model.pkl", "wb"))
    print("🎉 MODEL SAVED SUCCESSFULLY!")
except Exception as e:
    print("❌ Saving error:", e)
