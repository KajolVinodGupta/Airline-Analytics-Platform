import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import json
from utils.theme import inject_premium_ui

def app():
    inject_premium_ui()

    # -------------------------------------------------
    # Page Title
    # -------------------------------------------------
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title(" Flight Delay Prediction")
    with c2:
        # UPDATED CSS for "Grey Glassy" look
        st.markdown(
            """
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: #e0e0e0;
                padding: 8px 12px;
                border-radius: 16px;
                text-align: center;
                font-weight: 500;
                margin-top: 20px;
                font-size: 0.85em;
                backdrop-filter: blur(5px); /* Frosted effect */
            ">
            ML Powered
            </div>
            """, 
            unsafe_allow_html=True
        )
    st.caption("Predict if a flight will be delayed more than 15 minutes.")

    MODEL_PATH = Path("models/flight_delay_model.pkl")
    META_PATH = Path("models/model_info.json")

    # -------------------------------------------------
    # Load Model
    # -------------------------------------------------
    if not MODEL_PATH.exists():
        st.error("❌ Model not found. Train it first.")
        st.stop()

    pipeline = joblib.load(MODEL_PATH)

    # -------------------------------------------------
    # Model Metadata (Explainability / Audit)
    # -------------------------------------------------
    with st.expander("Model Information"):
        if META_PATH.exists():
            with open(META_PATH, "r") as f:
                meta = json.load(f)

            st.write(f"**Model Name:** {meta.get('model_name', 'N/A')}")
            st.write(f"**Algorithm:** {meta.get('algorithm', 'N/A')}")
            st.write(f"**Target:** {meta.get('target', 'N/A')}")
            st.write(f"**Accuracy:** {meta.get('accuracy', 'N/A')}")
            st.write(f"**Training Data:** {meta.get('training_data', 'N/A')}")
            st.write(f"**Last Trained:** {meta.get('last_trained', 'N/A')}")

            st.write("**Features Used:**")
            for feat in meta.get("features", []):
                st.write(f"- {feat}")
        else:
            st.warning("Model metadata file not found.")

    st.divider()

    # -------------------------------------------------
    # User Inputs
    # -------------------------------------------------
    airline = st.selectbox("Airline", ["AA", "DL", "UA", "B6", "WN", "AS"])
    origin = st.text_input("Origin Airport (IATA)", "JFK")
    destination = st.text_input("Destination Airport (IATA)", "LAX")

    distance = st.number_input("Distance (km)", 1, 10000, 2500)
    dep_delay = st.number_input("Departure Delay (min)", -10, 500, 0)
    taxi_out = st.number_input("Taxi-out Time (min)", 0, 60, 10)
    crs_dep_hour = st.slider("Scheduled Departure Hour", 0, 23, 12)
    month = st.slider("Month", 1, 12, 1)
    dayofweek = st.slider("Day of Week (0 = Monday)", 0, 6, 0)

    # -------------------------------------------------
    # Input DataFrame (MATCHES TRAINING)
    # -------------------------------------------------
    X = pd.DataFrame([{
        "airline": airline,
        "origin": origin,
        "destination": destination,
        "crs_dep_hour": str(crs_dep_hour),
        "distance": float(distance),
        "dep_delay": float(dep_delay),
        "taxi_out": float(taxi_out),
        "month": int(month),
        "dayofweek": int(dayofweek)
    }])[
        [
            "airline", "origin", "destination", "crs_dep_hour",
            "distance", "dep_delay", "taxi_out", "month", "dayofweek"
        ]
    ]

    st.markdown("""
        <style>
            
            /* Styles the button with a Blue/Purple Gradient */
            div.stButton > button {
                background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            }
            
            /* Button Hover Effect */
            div.stButton > button:hover {
                background: linear-gradient(90deg, #5b7ccf 0%, #2a3b5e 100%);
                box-shadow: 0 6px 12px rgba(75, 108, 183, 0.4);
                transform: translateY(-1px);
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------
    if st.button("Get Delay Prediction", type="secondary", width='stretch'):
        try:
            prob = pipeline.predict_proba(X)[0][1]
            pred = pipeline.predict(X)[0]

            # Result
            st.success(
                f"Prediction: {'Delayed' if pred == 1 else 'On-time'}"
            )
            st.info(f"Delay Probability: {prob:.2f}")

            # -------------------------------------------------
            # Explainability (Premium Glass Card)
            # -------------------------------------------------
            st.markdown(
                "<div class='glass-card fade-in'>"
                "<h3 style='margin-bottom:10px;'>🧠 Why this prediction?</h3>",
                unsafe_allow_html=True
            )

            reasons = []

            if dep_delay > 15:
                reasons.append((
                    "High departure delay",
                    "Initial delays often propagate through the flight schedule"
                ))

            if crs_dep_hour in [7, 8, 9, 17, 18, 19]:
                reasons.append((
                    "🚦 Peak-hour departure",
                    "Higher air traffic and runway congestion during peak hours"
                ))

            if taxi_out > 20:
                reasons.append((
                    "🛫 Long taxi-out time",
                    "Indicates congestion at the origin airport"
                ))

            if distance > 3000:
                reasons.append((
                    "🌍 Long-haul flight",
                    "Delays tend to amplify over longer distances"
                ))

            if not reasons:
                reasons.append((
                    "✅ Low-risk conditions",
                    "No strong delay indicators detected from input features"
                ))

            for title, desc in reasons:
                st.markdown(
                    f"""
                    <div style="
                        padding:10px;
                        margin-bottom:8px;
                        border-left:4px solid #6366f1;
                        background:rgba(99,102,241,0.05);
                        border-radius:6px;
                    ">
                        <strong>{title}</strong><br>
                        <span style="font-size:16px; opacity:0.85;">
                            {desc}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error("❌ Prediction failed — feature mismatch or data issue.")
            st.exception(e)
    # ------------------------------
    # Risk Contribution Summary
    # ------------------------------
    st.subheader("📊 Key Risk Contributors")

    risk_factors = []

    if dep_delay > 15:
        risk_factors.append(("Departure Delay", dep_delay))

    if taxi_out > 20:
        risk_factors.append(("Taxi-out Time", taxi_out))

    if crs_dep_hour in [7, 8, 9, 17, 18, 19]:
        risk_factors.append(("Peak Hour", crs_dep_hour))

    if distance > 3000:
        risk_factors.append(("Long Distance", distance))

    if risk_factors:
        rf_df = pd.DataFrame(risk_factors, columns=["Factor", "Value"])
        st.dataframe(rf_df)
    else:
        st.success("🟢 Flight conditions appear normal with low delay risk.")
        st.caption("All input features are within historically safe operating ranges.")

