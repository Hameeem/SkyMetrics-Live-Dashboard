import streamlit as st
import os
import base64

def get_plane_logo_base64():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "plane_logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{encoded}"
        except Exception:
            pass
    # High-quality fallback airplane icon
    return "https://img.icons8.com/color/96/000000/airplane.png"

def apply_custom_theme():
    """Applies vibrant Sky Blue & White Enterprise Theme with larger font sizes & high-contrast dark text."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                font-size: 17px !important;
            }

            .stApp {
                background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 50%, #ffffff 100%);
                color: #0f172a;
            }

            /* Global Form Label & Text High-Contrast Rules with Larger Font Sizes */
            label, .stMarkdown, .stMarkdown p, .stMarkdown span, .stSlider label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stCheckbox label, div[data-baseweb="input"] label {
                color: #0f172a !important;
                font-weight: 700 !important;
                font-size: 1.05rem !important;
            }

            /* High Contrast & Larger Input Fields */
            input, select, textarea, div[data-baseweb="select"] > div {
                background-color: #ffffff !important;
                color: #0f172a !important;
                border: 2px solid #0284c7 !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
                font-size: 1.05rem !important;
            }

            /* Slider Value Color & Number Inputs */
            div[data-testid="stWidgetLabel"] p {
                color: #0f172a !important;
                font-weight: 800 !important;
                font-size: 1.05rem !important;
            }

            .stNumberInput input, .stTextInput input {
                color: #0f172a !important;
                background-color: #ffffff !important;
                font-weight: 800 !important;
                font-size: 1.1rem !important;
            }

            /* Sky Blue & White Top Navigation Bar */
            .sky-header {
                background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                border-bottom: 4px solid #38bdf8;
                padding: 16px 30px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-radius: 12px;
                margin-bottom: 24px;
                box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.3);
            }

            .sky-logo-box {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .sky-logo-img {
                height: 52px;
                width: auto;
                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.25));
            }

            .sky-logo {
                font-size: 2.1rem;
                font-weight: 900;
                color: #ffffff;
                letter-spacing: -0.5px;
                line-height: 1.1;
            }

            .sky-logo span {
                color: #0f172a;
            }

            .nav-links {
                display: flex;
                gap: 26px;
                color: #ffffff;
                font-size: 1.05rem;
                font-weight: 700;
            }

            /* Glowing Live Radar Badge */
            .live-radar-badge {
                background: rgba(15, 23, 42, 0.9);
                border: 2px solid #22c55e;
                color: #ffffff;
                font-weight: 800;
                padding: 9px 20px;
                border-radius: 20px;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                box-shadow: 0 0 14px rgba(34, 197, 94, 0.5);
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .live-dot {
                height: 12px;
                width: 12px;
                background-color: #22c55e;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 10px #22c55e;
                animation: pulse-dot 1.8s infinite;
            }

            @keyframes pulse-dot {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
            }

            /* Clean White Container Card */
            .glass-card {
                background: #ffffff;
                border: 2px solid #bae6fd;
                border-radius: 12px;
                padding: 26px;
                margin-bottom: 22px;
                box-shadow: 0 10px 30px rgba(2, 132, 199, 0.08);
                color: #0f172a !important;
                font-size: 1.05rem !important;
            }

            /* Metric Display Card */
            .metric-card {
                background: #ffffff;
                border: 2px solid #e0f2fe;
                border-top: 5px solid #0284c7;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(2, 132, 199, 0.12);
            }

            .metric-card .value {
                font-size: 2.3rem;
                font-weight: 900;
                color: #0284c7;
            }

            .metric-card .label {
                font-size: 0.9rem;
                color: #334155;
                text-transform: uppercase;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin-top: 6px;
            }

            /* Sidebar Custom Styling with Larger Text */
            section[data-testid="stSidebar"] {
                background-color: #0369a1 !important;
                border-right: 3px solid #0284c7;
            }

            section[data-testid="stSidebar"] * {
                color: #ffffff !important;
                font-size: 1.05rem !important;
                font-weight: 600 !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_flightaware_navbar():
    logo_src = get_plane_logo_base64()
    st.markdown(f"""
        <div class="sky-header">
            <div class="sky-logo-box">
                <img src="{logo_src}" class="sky-logo-img" alt="SkyMetrics Logo Icon"/>
                <div class="sky-logo">Sky<span>Metrics</span></div>
            </div>
            <div class="nav-links">
                <span>Flight Tracking</span>
                <span>Airports & Weather</span>
                <span>ML Predictions</span>
                <span>ETL Pipelines</span>
                <span>AI Insights</span>
            </div>
            <div class="live-radar-badge"><span class="live-dot"></span> LIVE RADAR ACTIVE</div>
        </div>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    """Renders Sky Blue & White banner header for page modules."""
    render_flightaware_navbar()
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 24px 30px; border-radius: 12px; border-left: 6px solid #38bdf8; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.25);">
            <h2 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 2.0rem;">{title}</h2>
            <span style="color: #e0f2fe; font-size: 1.1rem; font-weight: 500;">{subtitle}</span>
        </div>
    """, unsafe_allow_html=True)
