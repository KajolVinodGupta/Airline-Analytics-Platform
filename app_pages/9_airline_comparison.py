import streamlit as st
import pandas as pd
from utils.run_query import run_query
from utils.theme import inject_premium_ui

def app():
    inject_premium_ui()
    st.header("Airline Comparison Dashboard")

    st.subheader("Revenue by Airline")
    df1 = run_query("SELECT airline, SUM(revenue) as total_rev FROM sales_data GROUP BY airline;")
    st.bar_chart(df1.set_index("airline"))

    st.subheader("Seats Sold by Airline")
    df2 = run_query("SELECT airline, SUM(seats_sold) as seats FROM sales_data GROUP BY airline;")
    st.line_chart(df2.set_index("airline"))

    st.subheader("Average Ticket Price")
    df3 = run_query("SELECT airline, AVG(ticket_price) as avg_price FROM sales_data GROUP BY airline;")
    st.dataframe(df3)
