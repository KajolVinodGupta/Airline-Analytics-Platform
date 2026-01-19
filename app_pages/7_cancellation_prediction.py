import streamlit as st
import pickle
import numpy as np
# Ensure this import path matches your project structure
from utils.theme import inject_premium_ui

def load_model():
    # Ensure this path to your model is correct
    return pickle.load(open("models/cancellation_model.pkl", "rb"))

def app():
    # Inject the base CSS (required for glass-card class etc.)
    inject_premium_ui()
    
    # 2. CUSTOM CSS: Hide Header & Style Button
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
            
            /* Remove extra padding at top since header is gone */
            .block-container {
                padding-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- 1. Header with "Grey Glass" ML Badge ---
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("Flight Cancellation Prediction")
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
    
    st.markdown("**Predict the likelihood of flight cancellation based on historical patterns.**")
    st.divider()

    try:
        bundle = load_model()
        model = bundle["model"]
        encoders = bundle["encoders"]
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'models/cancellation_model.pkl' exists.")
        return

    # --- 2. Optimized Layout (Columns) ---
    st.subheader("Flight Details")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Using .classes_ to get the list of categories the model knows
        airline = st.selectbox("Airline", encoders["Airline"].classes_)
    with col2:
        origin  = st.selectbox("Origin Airport", encoders["Origin"].classes_)
    with col3:
        dest    = st.selectbox("Destination Airport", encoders["Dest"].classes_)

    col4, col5 = st.columns(2)
    with col4:
        dep_delay = st.number_input("Departure Delay (mins)", 0, 600, value=0, help="Minutes delay before departure")
        distance  = st.number_input("Flight Distance (miles)", 1, 5000, value=500)
    with col5:
        month     = st.slider("Month", 1, 12, 1)
        dow       = st.slider("Day of Week (1=Mon, 7=Sun)", 1, 7, 1)

    st.markdown("---")

    # --- 3. Run Prediction Button (Changed color to neutral) ---
    # Changed type="primary" to type="secondary" for a neutral outline look
    if st.button("Will My Flight Be Cancelled?", type="secondary", width='stretch'):
        
        # --- Preprocessing & Prediction ---
        try:
            airline_enc = encoders["Airline"].transform([airline])[0]
            origin_enc  = encoders["Origin"].transform([origin])[0]
            dest_enc    = encoders["Dest"].transform([dest])[0]

            X = np.array([[airline_enc, origin_enc, dest_enc, 
                           dep_delay, distance, month, dow]])

            pred = model.predict(X)[0]
            prob = model.predict_proba(X)[0][1]
        except Exception as e:
            st.error(f"Error during prediction: {e}")
            st.stop()

        # --- Dynamic Result Styling ---
        is_cancelled = (pred == 1)
        
        # Define colors and icons based on the result
        if is_cancelled:
            result_color = "#ef4444"  # Red
            result_bg    = "rgba(239, 68, 68, 0.1)"
            status_text  = "High Risk: Flight Likely Cancelled"
            icon         = "❌"
        else:
            result_color = "#10b981"  # Green
            result_bg    = "rgba(16, 185, 129, 0.1)"
            status_text  = "Low Risk: Flight Likely On Time"
            icon         = "✅"

        # Display the main result box
        st.markdown(
            f"""
            <div style="
                background-color: {result_bg};
                border: 2px solid {result_color};
                padding: 20px;
                border-radius: 12px;
                text-align: center;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            ">
                <h2 style="color: {result_color}; margin:0; display:flex; align-items:center; justify-content:center; gap:10px;">
                    <span style="font-size: 1.3em;">{icon}</span> {status_text}
                </h2>
                <p style="margin-top:10px; font-size:1.1em; opacity:0.9;">
                    Cancellation Probability: <b>{prob*100:.1f}%</b>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Explainability Section ---
        st.markdown("### 🧠 Model Logic")
        
        reasons = []
        # Add business logic reasons based on inputs
        if dep_delay >= 60:
            reasons.append(f"Severe departure delay of {dep_delay} mins is a major risk factor.")
        elif dep_delay >= 30:
            reasons.append(f"Moderate departure delay of {dep_delay} mins increases risk slightly.")
            
        if distance < 300:
            reasons.append("Short-haul flights (<300 miles) are statistically easier for airlines to cancel.")
            
        if prob > 0.8:
            reasons.append("The model has very high confidence based on similar historical flights.")
            
        # Fallback reasons if no specific conditions met
        if not reasons and not is_cancelled:
            reasons.append("Flight parameters appear normal. No major risk factors detected.")
        elif not reasons and is_cancelled:
            reasons.append("Complex combination of factors detected by the ML model indicating risk.")

        # Render reasons with dynamic border color matching the result
        for r in reasons:
            st.markdown(
                f"""
                <div style="
                    padding: 12px 15px;
                    margin-bottom: 10px;
                    border-left: 5px solid {result_color};
                    background: rgba(255,255,255,0.05);
                    border-radius: 6px;
                    font-size: 0.95em;
                ">
                    {r}
                </div>
                """, 
                unsafe_allow_html=True
            )