# app_pages/1_flight_tracker.py
import streamlit as st
import math
import pydeck as pdk
from utils.fetch_flight_api import get_live_flights
from utils.ui import glass_card_start, glass_card_end, kpi_row, download_df_button

def app():
    st.subheader("Real-Time Flight Tracker")
    st.write("Live feed from API (OpenSky / AviationStack).")

    limit = st.slider("Flights to fetch", 10, 200, 50, key="ft_limit")

    glass_card_start()
    df = get_live_flights(limit=limit)

    if df is None or df.empty:
        st.warning("No live flights available or API key missing.")
        glass_card_end()
        return

    # KPI row
    total = len(df)
    uniques = df['airline'].nunique() if 'airline' in df.columns else 0
    avg_delay = df['delay'].dropna().mean() if 'delay' in df.columns else None 
    if avg_delay is not None and not math.isnan(avg_delay): 
        avg_delay_str = f"{avg_delay:.1f} min" 
    else: 
        avg_delay_str = "Not available for live data"

    kpi_row([ 
        {"label":"Live flights", "value":f"{total}"}, 
        {"label":"Active Airlines", "value":f"{uniques}"}, 
        {"label":"Avg Departure Delay", "value": avg_delay_str} 
    ])

    st.write("Live table (sample)")
    st.dataframe(df.head(200))
    download_df_button(df, filename="live_flights.csv", label="Download live flights CSV")

    # Map (if lat/lon available)
    if {"lat","lon"}.issubset(df.columns):
        df_map = df.dropna(subset=["lat","lon"])
        if not df_map.empty:
            st.subheader("Map view")
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_map,
                get_position=["lon","lat"],
                get_radius=5000,
                pickable=True
            )
            view_state = pdk.ViewState(latitude=df_map["lat"].mean(), longitude=df_map["lon"].mean(), zoom=3)
            r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text":"{flight_number}\n{airline}"})
            st.pydeck_chart(r)

    glass_card_end()
