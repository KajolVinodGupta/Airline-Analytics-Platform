import streamlit as st
from utils.run_query import run_query
import plotly.express as px
from utils.theme import inject_premium_ui

def app():
    inject_premium_ui()
    
    st.header("Sales Insights")
    st.write("Ticket sales & revenue breakdown")

    q = """
    SELECT flight_date, airline, route, seats_sold, revenue
    FROM sales_data
    ORDER BY flight_date DESC
    LIMIT 20000;
    """
    df = run_query(q)
    if df.empty:
        st.warning("No sales_data found.")
        return

    st.dataframe(df.head(100))

    st.subheader("Revenue by airline")
    rev = df.groupby("airline").revenue.sum().reset_index().sort_values("revenue", ascending=False)
    fig = px.bar(rev, x="airline", y="revenue", labels={"revenue":"Total Revenue"})
    st.plotly_chart(fig, width='stretch')

    st.subheader("Top routes by revenue")
    top_routes = df.groupby("route").revenue.sum().reset_index().sort_values("revenue", ascending=False).head(20)
    st.table(top_routes)
