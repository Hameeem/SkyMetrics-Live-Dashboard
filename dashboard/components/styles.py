import streamlit as st

def apply_custom_theme():
    """Applies FlightAware-inspired Deep Navy Enterprise theme to Streamlit app."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            .stApp {
                background-color: #0b1329;
                color: #f8fafc;
            }

            /* FlightAware Top Header Bar */
            .flightaware-header {
                background: linear-gradient(180deg, #001f44 0%, #001430 100%);
                border-bottom: 2px solid #0284c7;
                padding: 12px 24px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            }

            .flightaware-logo {
                font-size: 1.6rem;
                font-weight: 800;
                color: #ffffff;
                letter-spacing: -0.5px;
            }

            .flightaware-logo span {
                color: #38bdf8;
            }

            .nav-links {
                display: flex;
                gap: 20px;
                color: #cbd5e1;
                font-size: 0.9rem;
                font-weight: 500;
            }

            .signup-btn {
                background-color: #f59e0b;
                color: #000000;
                font-weight: 700;
                padding: 8px 18px;
                border-radius: 6px;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }

            /* Glassmorphism Container Card */
            .glass-card {
                background: rgba(15, 23, 42, 0.85);
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            }

            /* Metric Display Card */
            .metric-card {
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 8px;
                padding: 16px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            }

            .metric-card .value {
                font-size: 1.8rem;
                font-weight: 800;
                color: #38bdf8;
            }

            .metric-card .label {
                font-size: 0.8rem;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 4px;
            }

            /* Status Badges */
            .badge-enroute {
                background-color: rgba(34, 197, 94, 0.2);
                color: #4ade80;
                border: 1px solid rgba(34, 197, 94, 0.4);
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            }

            .badge-delayed {
                background-color: rgba(239, 68, 68, 0.2);
                color: #f87171;
                border: 1px solid rgba(239, 68, 68, 0.4);
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            }

            .badge-approach {
                background-color: rgba(245, 158, 11, 0.2);
                color: #fbbf24;
                border: 1px solid rgba(245, 158, 11, 0.4);
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 0.75rem;
                font-weight: 600;
            }

            /* Sidebar Custom Styling */
            section[data-testid="stSidebar"] {
                background-color: #001430 !important;
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

def render_flightaware_navbar():
    st.markdown("""
        <div class="flightaware-header">
            <div class="flightaware-logo">✈️ Sky<span>Metrics</span></div>
            <div class="nav-links">
                <span>Flight Tracking</span>
                <span>Airports & Weather</span>
                <span>ML Predictions</span>
                <span>ETL Pipelines</span>
                <span>AI Insights</span>
            </div>
            <div class="signup-btn">Pro Operations</div>
        </div>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    """Renders FlightAware-styled banner header for page modules."""
    render_flightaware_navbar()
    st.markdown(f"""
        <div style="background: linear-gradient(90deg, #001f44 0%, #003366 100%); padding: 18px 24px; border-radius: 8px; border-left: 5px solid #0284c7; margin-bottom: 20px;">
            <h2 style="margin: 0; color: #ffffff; font-weight: 800;">{title}</h2>
            <span style="color: #cbd5e1; font-size: 0.95rem;">{subtitle}</span>
        </div>
    """, unsafe_allow_html=True)
