# utils/theme.py
import streamlit as st

def inject_premium_ui():
    css = r"""
    <style>
    /* --- Fonts --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    /* Main background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }

    /* --- Sidebar premium container - REMOVED DARK BACKGROUND --- */
    .premium-sidebar {
        background: #0E1117; !important;  /* Changed from dark gradient */
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    
    .premium-sidebar h3 {
        color: #FAFAFA !important;  /* Changed to dark color */
        margin-bottom: 15px !important;
        font-weight: 700 !important;
    }
    
    .premium-sidebar h4 {
        color: #FAFAFA !important;  /* Changed to medium gray */
        margin: 15px 0 10px 0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    /* Style Streamlit buttons in sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0E1117 !important;
        border-right: 1px solid #e5e7eb !important;
    }

    /* Custom button styling - LIGHT THEME */
    section[data-testid="stSidebar"] button {
        background: #0E1117 !important;
        color: #FAFAFA !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        margin: 6px 0 !important;
        text-align: left !important;
        transition: all 0.3s ease !important;
        font-size: 14px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }

    section[data-testid="stSidebar"] button:hover {
        background: #0E1117;
        color: #FAFAFA !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
        border: 1px solid #9ca3af !important;
    }

    /* Active page button style */
    section[data-testid="stSidebar"] button:active,
    section[data-testid="stSidebar"] button:focus:not(:active) {
        background: #0E1117;
        color: #FAFAFA !important;
        border: 1px solid #6366f1 !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
    }

    /* --- Floating header --- */
    .premium-header {
        background: linear-gradient(90deg, rgba(99,102,241,0.06), rgba(124,58,237,0.04));
        border-radius: 10px;
        padding: 16px 22px;
        margin-bottom: 18px;
        display:flex;
        align-items:center;
        gap:18px;
        box-shadow: 0 8px 20px rgba(2,6,23,0.04);
        backdrop-filter: blur(6px);
    }
    .premium-title {
        font-weight:800;
        font-size:28px;
        color: #FAFAFA;
        margin:0;
    }
    .premium-sub {
        color:#FAFAFA;
        margin:0;
        font-size:14px;
    }

    /* --- Glass card --- */
    .glass-card {
        background: #0E1117;
        transition: transform .18s ease, box-shadow .18s ease;
        margin-bottom: 25px;
    }
    .glass-card:hover { transform: translateY(-6px); box-shadow: 0 16px 36px rgba(2,6,23,0.08); }

    /* KPI */
    .kpi-row { display:flex; gap:14px; flex-wrap:wrap; margin-bottom:16px; }
    .kpi { flex:0 1 220px; padding:14px; border-radius:10px; background: rgba(26, 31, 44, 0.6); box-shadow:0 8px 22px rgba(2,6,23,0.04); }
    .kpi h3 { margin:0; font-size:14px; font-weight:600; color: #a0a0a0;}
    .kpi p { margin:6px 0 0 0; font-size:18px; font-weight:800; color: #ffffff;}

    /* Table header style */
    .stDataFrame table {
      border-radius: 8px;
      overflow: hidden;
    }

    /* Entry animation */
    .fade-in {
      animation: fadeIn .38s ease both;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0px); }
    }

    /* Small screens */
    @media (max-width: 800px) {
      .premium-title { font-size:20px; }
      .kpi { flex: 1 1 100%; }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)