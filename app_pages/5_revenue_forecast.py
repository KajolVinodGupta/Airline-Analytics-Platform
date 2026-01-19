import streamlit as st
from utils.load_models import load_revenue_model
from utils.run_query import run_query
import pandas as pd
import plotly.express as px
from utils.theme import inject_premium_ui

def app():
    inject_premium_ui()
    st.header("Revenue Forecast")
    st.write("Forecast monthly revenue using the saved Prophet model.")

    model = load_revenue_model()
    if model is None:
        st.warning("Revenue forecast model not found in /models. Train and save 'revenue_forecast.pkl' first.")
        return

    # get historical series
    q = """
    SELECT flight_date, revenue FROM sales_data
    WHERE flight_date IS NOT NULL
    """
    hist = run_query(q)
    if hist.empty:
        st.warning("No sales_data present.")
        return

    hist['flight_date'] = pd.to_datetime(hist['flight_date'])
    ts = hist.groupby(pd.Grouper(key='flight_date', freq='ME')).revenue.sum().reset_index().rename(columns={'flight_date':'ds','revenue':'y'})
    st.subheader("Historical monthly revenue")
    st.line_chart(ts.set_index('ds')['y'])

    # Forecast
    periods = st.selectbox("Forecast horizon (months)", [1,3,6,12], index=1)
    future = model.make_future_dataframe(periods=periods, freq='ME')
    forecast = model.predict(future)
    forecast_display = forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(periods)
    st.subheader("Forecasted revenue (next periods)")
    st.dataframe(forecast_display)

    fig = px.line(forecast, x='ds', y=['yhat','yhat_lower','yhat_upper'])
    st.plotly_chart(fig, width='stretch')
