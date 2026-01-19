# app_pages/template.py
import streamlit as st
from utils.ui import kpi_row, glass_card_start, glass_card_end, styled_dataframe, download_df_button

def app():
    """Template for consistent page layout."""
    
    # Page title
    st.markdown("## 📊 Page Title")
    st.markdown("---")
    
    # KPI Row Example
    kpi_row([
        {"label": "Live Flights", "value": "50", "meta": "Currently tracking"},
        {"label": "Active Airlines", "value": "28", "meta": "Worldwide"},
        {"label": "Avg Departure Delay", "value": "6.0 min", "meta": "± 2.1 min"}
    ])
    
    # Glass Card Example
    glass_card_start()
    st.markdown("### 📈 Live Data")
    st.markdown("This is an example of a glass card with data inside.")
    
    # Example dataframe (replace with your actual data)
    import pandas as pd
    example_data = pd.DataFrame({
        "flight_number": ["AA123", "DL456", "UA789"],
        "airline": ["American Airlines", "Delta", "United"],
        "status": ["On Time", "Delayed", "Scheduled"]
    })
    
    styled_dataframe(example_data)
    
    download_df_button(example_data, "example_data.csv", "📥 Download Example Data")
    glass_card_end()
    
    # Another section
    st.markdown("---")
    st.markdown("### 🔧 Configuration")
    
    # Example inputs
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Number of flights to fetch", min_value=1, max_value=1000, value=50)
    with col2:
        st.selectbox("Airline filter", ["All Airlines", "American", "Delta", "United"])