import streamlit as st
from utils.theme import inject_premium_ui
import base64

def app():
    inject_premium_ui()
    st.set_page_config(layout="wide")

    st.header("Power BI Dashboard (Report View)")
    

    st.write(
        "Due to organizational restrictions, the Power BI report is shared "
        "as a downloadable and viewable PDF generated directly from Power BI Desktop."
    )

    st.caption("Report exported directly from Power BI Desktop")

    pdf_path = "dashboard/Airline_Analytics_Dashboard_PowerBI.pdf"

    # Read PDF
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    # Download button
    st.download_button(
        label="Download Power BI Report (PDF)",
        data=pdf_bytes,
        file_name="Airline_Analytics_PowerBI_Report.pdf",
        mime="application/pdf"
    )

    st.divider()

    st.subheader("Revenue Overview")
    st.image(
        "dashboard/powerbi_revenue.png",
        width='stretch'
    )

    st.divider()

    st.subheader("Operational KPIs")
    st.image(
        "dashboard/powerbi_operations.png",
        width='stretch'
    )

    st.divider()

    st.subheader("Airline Comparison")
    st.image(
        "dashboard/powerbi_comparison.png",
        width='stretch'
    )