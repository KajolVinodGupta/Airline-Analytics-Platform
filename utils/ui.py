# utils/ui.py
import streamlit as st
from importlib import import_module

def premium_sidebar_nav(pages_dict):
    """
    Renders the premium sidebar (buttons) with Material Icons and returns selected page key.
    """
    st.sidebar.markdown("<h2 style='text-align: center;'>Airline Analytics Platform</h2>", unsafe_allow_html=True)
    st.sidebar.divider()
    
    if "current_page" not in st.session_state:
        st.session_state.current_page = list(pages_dict.keys())[0]

    # --- Section 1: Flight Tracking ---
    st.sidebar.markdown("### Flight Tracking")
    
    # Define Material Icons for the first 6 pages
    # You can find more icons at fonts.google.com/icons
    section_1_icons = {
        "Real-Time Flight Tracker": ":material/flight_takeoff:",
        "Delay Analyzer": ":material/timer:",
        "Delay Prediction (ML)": ":material/psychology:",  # or :material/smart_toy:
        "Sales Insights": ":material/payments:",
        "Revenue Forecast": ":material/trending_up:",
        "Power BI Dashboard": ":material/analytics:"
    }

    # Iterate through first 6 pages
    for page_name in list(pages_dict.keys())[:6]:
        # Get icon, default to a generic star if missing
        icon_code = section_1_icons.get(page_name, ":material/star:")
        
        # Check if this button is currently active
        is_active = (st.session_state.current_page == page_name)
        
        if st.sidebar.button(
            page_name, 
            icon=icon_code,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary" # Highlight active button
        ):
            st.session_state.current_page = page_name
            st.rerun()

    st.sidebar.divider()
    
    # --- Section 2: Prediction & Comparison ---
    st.sidebar.markdown("### Prediction & Comparison")
    
    section_2_icons = {
        "Cancellation Prediction (ML)": ":material/cancel_schedule_send:",
        "Weather Impact Analyzer": ":material/thunderstorm:",
        "Airline Comparison": ":material/compare_arrows:"
    }

    # Iterate through remaining pages
    for page_name in list(pages_dict.keys())[6:]:
        icon_code = section_2_icons.get(page_name, ":material/star:")
        
        is_active = (st.session_state.current_page == page_name)

        if st.sidebar.button(
            page_name, 
            icon=icon_code,
            key=f"nav_{page_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_page = page_name
            st.rerun()


def premium_header(title, subtitle=None):
    html = "<div class='premium-header fade-in'>"
    html += f"<div><h1 class='premium-title'>{title}</h1>"
    if subtitle:
        html += f"<div class='premium-sub'>{subtitle}</div>"
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


def kpi_row(kpis:list):
    """
    kpis: list of dict { 'label':str, 'value':str, 'meta':str(optional) }
    """
    html = "<div class='kpi-row'>"
    for k in kpis:
        label = k.get("label","")
        value = k.get("value","")
        meta = k.get("meta","")
        html += "<div class='kpi glass-card'>"
        html += f"<h3>{label}</h3>"
        html += f"<p>{value}</p>"
        if meta:
            html += f"<small style='color:#6b7280'>{meta}</small>"
        html += "</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def glass_card_start():
    st.markdown("<div class='glass-card fade-in'>", unsafe_allow_html=True)

def glass_card_end():
    st.markdown("</div>", unsafe_allow_html=True)


def download_df_button(df, filename="data.csv", label="Download CSV"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label=label, data=csv, file_name=filename, mime='text/csv')