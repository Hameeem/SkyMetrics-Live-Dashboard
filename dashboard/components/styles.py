import streamlit as st
import os
import base64

def get_flight_trail_logo_base64():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "flight_trail_white.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{encoded}"
        except Exception:
            pass
    return "https://img.icons8.com/color/96/000000/airplane.png"

def apply_custom_theme():
    """Applies vibrant Sky Blue & White Enterprise Theme with 2-row layout and zero text overlap."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            .stApp {
                background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 50%, #ffffff 100%);
                color: #0f172a;
            }

            /* Global Form Label & Text High-Contrast Rules */
            label, .stMarkdown, .stMarkdown p, .stMarkdown span, .stSlider label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stCheckbox label, div[data-baseweb="input"] label {
                color: #0f172a !important;
                font-weight: 700 !important;
                font-size: 0.98rem !important;
            }

            /* High Contrast Input Fields */
            input, select, textarea, div[data-baseweb="select"] > div {
                background-color: #ffffff !important;
                color: #0f172a !important;
                border: 2px solid #0284c7 !important;
                border-radius: 8px !important;
                font-weight: 700 !important;
            }

            /* TOP BRANDING BAR (Row 1) - Isolated Logo & Name */
            .sky-top-bar {
                background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                padding: 16px 28px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-radius: 14px 14px 0 0;
                box-shadow: 0 4px 15px rgba(2, 132, 199, 0.2);
            }

            .sky-branding {
                display: flex;
                align-items: center;
                gap: 16px;
            }

            /* Bigger Airplane Logo Icon */
            .trail-logo-large {
                height: 68px;
                width: auto;
                filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
            }

            .sky-brand-name {
                font-size: 2.6rem;
                font-weight: 900;
                color: #ffffff;
                letter-spacing: -0.5px;
                margin: 0;
                line-height: 1;
            }

            .sky-brand-name span {
                color: #0f172a;
                font-weight: 900;
            }

            /* Glowing Live Radar Badge */
            .live-radar-badge {
                background: #0f172a;
                border: 2px solid #22c55e;
                color: #ffffff;
                font-weight: 800;
                padding: 8px 18px;
                border-radius: 20px;
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                box-shadow: 0 0 14px rgba(34, 197, 94, 0.5);
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .live-dot {
                height: 10px;
                width: 10px;
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

            /* CATEGORY NAVIGATION SUB-BAR (Row 2) - Clean Horizontal Links */
            .sky-sub-nav {
                background: #0369a1;
                border-top: 2px solid #38bdf8;
                border-bottom: 4px solid #0284c7;
                padding: 10px 28px;
                display: flex;
                align-items: center;
                justify-content: space-around;
                border-radius: 0 0 14px 14px;
                margin-bottom: 24px;
                box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.3);
            }

            .sub-nav-pill {
                color: #ffffff;
                font-size: 0.95rem;
                font-weight: 700;
                background: rgba(255, 255, 255, 0.12);
                border: 1px solid rgba(255, 255, 255, 0.25);
                padding: 6px 16px;
                border-radius: 20px;
                text-decoration: none;
                white-space: nowrap;
            }

            /* Metric Display Card */
            .metric-card {
                background: #ffffff;
                border: 2px solid #e0f2fe;
                border-top: 5px solid #0284c7;
                border-radius: 12px;
                padding: 22px 14px;
                text-align: center;
                box-shadow: 0 8px 24px rgba(2, 132, 199, 0.12);
            }

            .metric-card .value {
                font-size: 2.5rem;
                font-weight: 900;
                color: #0284c7;
                line-height: 1;
            }

            .metric-card .label {
                font-size: 0.82rem;
                color: #334155;
                text-transform: uppercase;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin-top: 10px;
            }

            /* Container Card */
            .glass-card {
                background: #ffffff;
                border: 2px solid #bae6fd;
                border-radius: 12px;
                padding: 26px;
                margin-bottom: 22px;
                box-shadow: 0 10px 30px rgba(2, 132, 199, 0.08);
                color: #0f172a !important;
            }

            /* Sidebar Custom Styling */
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
    logo_src = get_flight_trail_logo_base64()
    st.markdown(f"""
        <div>
            <!-- ROW 1: TOP BRANDING BAR WITH BIGGER LOGO & NAME -->
            <div class="sky-top-bar">
                <div class="sky-branding">
                    <img src="{logo_src}" class="trail-logo-large" alt="Flight Trail Logo"/>
                    <h1 class="sky-brand-name">Sky<span>Metrics</span></h1>
                </div>
                <div class="live-radar-badge"><span class="live-dot"></span> LIVE RADAR ACTIVE</div>
            </div>
            <!-- ROW 2: CATEGORY NAVIGATION SUB-BAR -->
            <div class="sky-sub-nav">
                <div class="sub-nav-pill">✈️ Flight Tracking</div>
                <div class="sub-nav-pill">🌤️ Airports & Weather</div>
                <div class="sub-nav-pill">🤖 ML Predictions</div>
                <div class="sub-nav-pill">⚡ ETL Pipelines</div>
                <div class="sub-nav-pill">💡 AI Insights</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    """Renders Sky Blue & White banner header for page modules."""
    render_flightaware_navbar()
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 24px 30px; border-radius: 12px; border-left: 6px solid #38bdf8; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.25);">
            <h2 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 2.0rem;">{title}</h2>
            <span style="color: #e0f2fe; font-size: 1.05rem; font-weight: 500;">{subtitle}</span>
        </div>
    """, unsafe_allow_html=True)
