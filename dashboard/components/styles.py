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

def get_dark_trail_logo_base64():
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "trail_logo.png")
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/png;base64,{encoded}"
        except Exception:
            pass
    return get_flight_trail_logo_base64()

def apply_custom_theme():
    """Applies Enterprise Aviation Command Center White & Minimal Theme (#F8FAFC background)."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            /* Main Background: Clean Bright Aviation Slate (#F8FAFC) */
            .stApp {
                background-color: #F8FAFC !important;
                color: #111827 !important;
            }

            /* Global Typography & Input Controls */
            label, .stMarkdown p, .stMarkdown span, .stSlider label, .stTextInput label, .stNumberInput label, .stSelectbox label, .stCheckbox label, div[data-baseweb="input"] label {
                color: #111827 !important;
                font-weight: 700 !important;
                font-size: 0.95rem !important;
            }

            /* Modern Inputs & Dropdowns */
            input, select, textarea, div[data-baseweb="select"] > div {
                background-color: #FFFFFF !important;
                color: #111827 !important;
                border: 1px solid #E5E7EB !important;
                border-radius: 10px !important;
                font-weight: 600 !important;
                box-shadow: 0 2px 5px rgba(0,0,0,0.02) !important;
                transition: all 0.2s ease !important;
            }

            input:focus, select:focus, div[data-baseweb="select"]:focus {
                border-color: #1E88E5 !important;
                box-shadow: 0 0 0 3px rgba(30, 136, 229, 0.15) !important;
            }

            /* HERO SECTION - Enterprise Aviation Command Center Header */
            .sky-hero-card {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 20px;
                padding: 28px 36px;
                margin-bottom: 24px;
                box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.05);
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 20px;
            }

            .hero-left {
                display: flex;
                align-items: center;
                gap: 16px;
            }

            .hero-logo-img {
                height: 72px;
                width: auto;
                filter: drop-shadow(0 4px 6px rgba(0,0,0,0.08));
            }

            .hero-title-box {
                display: flex;
                flex-direction: column;
            }

            .hero-title-main {
                font-size: 2.2rem;
                font-weight: 900;
                color: #111827;
                letter-spacing: -0.5px;
                margin: 0;
                line-height: 1.1;
            }

            .hero-title-main span {
                color: #1E88E5;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                font-weight: 700;
                color: #1E88E5;
                margin-top: 4px;
            }

            .hero-description {
                font-size: 0.9rem;
                color: #6B7280;
                margin-top: 2px;
            }

            /* Floating Live Radar Status Card (Dark Glassmorphism) */
            .live-radar-floating {
                background: #0F172A;
                border: 2px solid #00C853;
                color: #FFFFFF;
                font-weight: 800;
                padding: 12px 24px;
                border-radius: 16px;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                box-shadow: 0 8px 24px rgba(0, 200, 83, 0.25);
                display: flex;
                align-items: center;
                gap: 10px;
                white-space: nowrap;
            }

            .live-dot-green {
                height: 12px;
                width: 12px;
                background-color: #00C853;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 10px #00C853;
                animation: pulse-dot 1.8s infinite;
            }

            @keyframes pulse-dot {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 200, 83, 0.7); }
                70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(0, 200, 83, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 200, 83, 0); }
            }

            /* Floating Navigation Shortcut Pills */
            .nav-shortcuts-row {
                display: flex;
                align-items: center;
                justify-content: flex-start;
                gap: 14px;
                margin-bottom: 24px;
                flex-wrap: wrap;
            }

            .nav-pill-item {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 20px;
                padding: 8px 20px;
                font-size: 0.9rem;
                font-weight: 700;
                color: #1E88E5;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
                transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
                cursor: pointer;
            }

            .nav-pill-item:hover {
                transform: translateY(-2px);
                border-color: #1E88E5;
                box-shadow: 0 8px 20px rgba(30, 136, 229, 0.12);
            }

            /* PREMIUM KPI METRIC CARDS (20px radius, white background, top accent border) */
            .metric-card-premium {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-top: 4px solid #1E88E5;
                border-radius: 20px;
                padding: 24px 16px;
                text-align: center;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }

            .metric-card-premium:hover {
                transform: translateY(-3px);
                box-shadow: 0 14px 30px -5px rgba(30, 136, 229, 0.12);
            }

            .metric-card-premium .value {
                font-size: 2.6rem;
                font-weight: 900;
                color: #1E88E5;
                line-height: 1;
            }

            .metric-card-premium .label {
                font-size: 0.8rem;
                color: #6B7280;
                text-transform: uppercase;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin-top: 10px;
            }

            /* Backward compatibility alias for metric-card */
            .metric-card {
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-top: 4px solid #1E88E5;
                border-radius: 20px;
                padding: 24px 16px;
                text-align: center;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
            }
            .metric-card .value {
                font-size: 2.6rem;
                font-weight: 900;
                color: #1E88E5;
                line-height: 1;
            }
            .metric-card .label {
                font-size: 0.8rem;
                color: #6B7280;
                text-transform: uppercase;
                font-weight: 800;
                letter-spacing: 0.5px;
                margin-top: 10px;
            }

            /* PREMIUM WHITE CONTENT CARD CONTAINER */
            .glass-card {
                background: #FFFFFF !important;
                border: 1px solid #E5E7EB !important;
                border-radius: 20px !important;
                padding: 26px !important;
                margin-bottom: 24px !important;
                box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.04) !important;
                color: #111827 !important;
            }

            /* Status Badges */
            .badge-enroute {
                background-color: #E8F5E9;
                color: #00C853;
                border: 1px solid #A5D6A7;
                padding: 5px 14px;
                border-radius: 14px;
                font-size: 0.78rem;
                font-weight: 800;
            }

            .badge-delayed {
                background-color: #FFEBEE;
                color: #E53935;
                border: 1px solid #FFCDD2;
                padding: 5px 14px;
                border-radius: 14px;
                font-size: 0.78rem;
                font-weight: 800;
            }

            .badge-approach {
                background-color: #FFF3E0;
                color: #FB8C00;
                border: 1px solid #FFE0B2;
                padding: 5px 14px;
                border-radius: 14px;
                font-size: 0.78rem;
                font-weight: 800;
            }

            /* PREMIUM DEEP AVIATION BLUE SIDEBAR */
            section[data-testid="stSidebar"] {
                background: linear-gradient(180deg, #0C4A6E 0%, #0284C7 100%) !important;
                border-right: 1px solid #0369A1;
            }

            section[data-testid="stSidebar"] * {
                color: #FFFFFF !important;
                font-size: 0.98rem !important;
                font-weight: 600 !important;
            }

            /* Sidebar Active Page Pill Highlight */
            div[data-testid="stSidebarNav"] ul li div[aria-selected="true"] {
                background: rgba(255, 255, 255, 0.25) !important;
                border-left: 4px solid #38BDF8 !important;
                border-radius: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_flightaware_navbar():
    logo_src = get_dark_trail_logo_base64()
    st.markdown(f"""
        <div>
            <!-- PREMIUM HERO HEADER CARD -->
            <div class="sky-hero-card">
                <div class="hero-left">
                    <img src="{logo_src}" class="hero-logo-img" alt="SkyMetrics Logo"/>
                    <div class="hero-title-box">
                        <h1 class="hero-title-main">Sky<span>Metrics</span></h1>
                        <span class="hero-subtitle">Flight Operations Command Center</span>
                        <span class="hero-description">Real-Time Aviation Intelligence Platform</span>
                    </div>
                </div>
                <div class="live-radar-floating">
                    <span class="live-dot-green"></span> LIVE RADAR ACTIVE
                </div>
            </div>
            <!-- FLOATING SHORTCUT PILLS -->
            <div class="nav-shortcuts-row">
                <div class="nav-pill-item">✈️ Flight Tracking</div>
                <div class="nav-pill-item">🌤️ Airports & Weather</div>
                <div class="nav-pill-item">🤖 ML Predictions</div>
                <div class="nav-pill-item">⚡ ETL Pipelines</div>
                <div class="nav-pill-item">💡 AI Insights</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    """Renders Hero Header and Module Sub-Banner."""
    render_flightaware_navbar()
    st.markdown(f"""
        <div style="background: #FFFFFF; padding: 22px 28px; border-radius: 16px; border: 1px solid #E5E7EB; border-left: 6px solid #1E88E5; margin-bottom: 24px; box-shadow: 0 8px 20px rgba(0,0,0,0.03);">
            <h2 style="margin: 0; color: #111827; font-weight: 800; font-size: 1.8rem;">{title}</h2>
            <span style="color: #6B7280; font-size: 1rem; font-weight: 500;">{subtitle}</span>
        </div>
    """, unsafe_allow_html=True)
