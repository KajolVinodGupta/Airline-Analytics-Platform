# app_pages/2_delay_analyzer.py
import streamlit as st
from utils.run_query import run_query
from utils.ui import glass_card_start, glass_card_end, kpi_row, download_df_button
import plotly.express as px
import pandas as pd

def app():
    st.subheader("Delay Analyzer")
    st.write("Analyze historical delay patterns from `flight_delay`.")

    glass_card_start()
    q = """
    SELECT flight_date, origin, destination, arr_delay, dep_delay, cancelled
    FROM flight_delay
    WHERE arr_delay IS NOT NULL
    ORDER BY flight_date DESC
    LIMIT 50000;
    """
    df = run_query(q)

    if df.empty:
        st.warning("No flight_history data found. Load data into SQL first.")
        glass_card_end()
        return

    # KPIs
    total_rows = len(df)
    avg_arr_delay = df['arr_delay'].mean()
    cancel_rate = df['cancelled'].mean() * 100 if 'cancelled' in df.columns else 0
    kpi_row([
        {"label":"Records loaded", "value":f"{total_rows:,}"},
        {"label":"Avg Arrival Delay", "value":f"{avg_arr_delay:.2f} min"},
        {"label":"Cancellation Rate", "value":f"{cancel_rate:.2f}%"}
    ])

    st.write("Sample data")
    st.dataframe(df.head(200))
    download_df_button(df, filename="delay_sample.csv", label="Download sample CSV")

    # top routes by avg delay
    by_route = df.groupby(["origin","destination"]).arr_delay.mean().reset_index()
    by_route["route"] = by_route["origin"] + "-" + by_route["destination"]
    top = by_route.sort_values("arr_delay", ascending=False).head(20)
    st.subheader("Top 20 routes by avg arrival delay")
    fig = px.bar(top, x="route", y="arr_delay", labels={"arr_delay":"Avg Arrival Delay (min)"})
    st.plotly_chart(fig, width='stretch')

    st.subheader("Arrival delay distribution")
    fig2 = px.histogram(df, x="arr_delay", nbins=80)
    st.plotly_chart(fig2, width='stretch')

    glass_card_end()
