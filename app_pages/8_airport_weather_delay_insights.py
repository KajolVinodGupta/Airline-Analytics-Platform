import streamlit as st
from utils.fetch_weather_api import fetch_weather
from utils.theme import inject_premium_ui

def app():
    inject_premium_ui()
    st.title("🌤 Weather Impact Analyzer")

    iata = st.text_input("Enter Airport Code (IATA):", "JFK")

    if st.button("Fetch Weather"):
        weather, error = fetch_weather(iata)

        if error:
            st.error(error)
            return

        st.success(f"Live Weather Data for {iata}")

        # Display weather metrics
        st.metric("Temperature (°C)", weather.get("temperature"))
        st.metric("Wind Speed (km/h)", weather.get("wind_speed"))
        st.metric("Visibility (km)", weather.get("visibility"))
        st.metric("Precipitation (mm)", weather.get("precip"))
        st.metric("Condition", weather.get("weather_descriptions", ["Unknown"])[0])

        st.write("---")
        

        # Simple reasoning system
        st.markdown(
            "<div class='glass-card fade-in'>"
            "<h3>✈️ Delay Risk Explanation</h3>",
            unsafe_allow_html=True
        )

        risk_score = 0
        reasons = []

        if weather.get("precip", 0) > 2:
            risk_score += 2
            reasons.append("🌧 Heavy precipitation affects runway operations")

        if weather.get("wind_speed", 0) > 40:
            risk_score += 2
            reasons.append("💨 Strong winds impact aircraft stability")

        if weather.get("visibility", 10) < 5:
            risk_score += 1
            reasons.append("🌫 Low visibility affects landing safety")

        if risk_score == 0:
            st.success("✨ Low Delay Risk")
        elif risk_score <= 2:
            st.warning("⚠️ Moderate Delay Risk")
        else:
            st.error("❌ High Delay Risk")

        for r in reasons:
            st.markdown(
                f"""
                <div style="
                    padding:10px;
                    margin-bottom:8px;
                    border-left:4px solid #0ea5e9;
                    background:rgba(14,165,233,0.08);
                    border-radius:6px;
                ">
                    {r}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)
