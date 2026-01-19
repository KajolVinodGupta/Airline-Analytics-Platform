# app.py
import streamlit as st
from importlib import import_module
from utils.theme import inject_premium_ui
from utils.ui import premium_sidebar_nav, premium_header

# Inject CSS first
inject_premium_ui()

st.set_page_config(page_title="Airline Analytics Platform", page_icon="assets/plane.png", layout="wide")

PAGES = {
    "Real-Time Flight Tracker": "app_pages.1_flight_tracker",
    "Delay Analyzer": "app_pages.2_delay_analyzer",
    "Delay Prediction": "app_pages.3_delay_prediction",
    "Sales Insights": "app_pages.4_sales_insights",
    "Revenue Forecast": "app_pages.5_revenue_forecast",
    "Power BI Dashboard": "app_pages.6_powerbi_dashboard",
    "Cancellation Prediction": "app_pages.7_cancellation_prediction",
    "Weather Impact Analyzer": "app_pages.8_airport_weather_delay_insights",
    "Airline Comparison": "app_pages.9_airline_comparison"
}

# render premium sidebar
premium_sidebar_nav(PAGES)

# load selected page
selected = st.session_state.get("current_page", list(PAGES.keys())[0])
try:
    module = import_module(PAGES[selected])
    module.app()
except KeyError:
    # Fallback to first page if selected page not found
    module = import_module(PAGES[list(PAGES.keys())[0]])
    module.app()