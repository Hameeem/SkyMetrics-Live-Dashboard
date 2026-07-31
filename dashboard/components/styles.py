import streamlit as st
import os

def apply_custom_theme():
    """Applies vibrant Sky Blue & White Enterprise Theme to Streamlit app."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            .stApp {
                background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 50%, #ffffff 100%);
                color: #0f172a;
            }

            /* Sky Blue & White Top Navigation Bar */
            .sky-header {
                background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
                border-bottom: 3px solid #38bdf8;
                padding: 14px 28px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                border-radius: 12px;
                margin-bottom: 24px;
                box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.3);
            }

            .sky-logo {
                font-size: 1.7rem;
                font-weight: 800;
                color: #ffffff;
                letter-spacing: -0.5px;
            }

            .sky-logo span {
                color: #bae6fd;
            }

            .nav-links {
                display: flex;
                gap: 22px;
                color: #e0f2fe;
                font-size: 0.95rem;
                font-weight: 600;
            }

            .signup-btn {
                background-color: #ffffff;
                color: #0284c7;
                font-weight: 800;
                padding: 9px 20px;
                border-radius: 8px;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            }

            /* Clean White Container Card */
            .glass-card {
                background: #ffffff;
                border: 1px solid #bae6fd;
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(2, 132, 199, 0.08);
            }

            /* Metric Display Card */
            .metric-card {
                background: #ffffff;
                border: 2px solid #e0f2fe;
                border-top: 4px solid #0284c7;
                border-radius: 10px;
                padding: 18px;
                text-align: center;
                box-shadow: 0 6px 18px rgba(2, 132, 199, 0.1);
            }

            .metric-card .value {
                font-size: 2.1rem;
                font-weight: 800;
                color: #0284c7;
            }

            .metric-card .label {
                font-size: 0.82rem;
                color: #475569;
                text-transform: uppercase;
                font-weight: 700;
                letter-spacing: 0.5px;
                margin-top: 4px;
            }

            /* Status Badges */
            .badge-enroute {
                background-color: #dcfce7;
                color: #15803d;
                border: 1px solid #86efac;
                padding: 4px 12px;
                border-radius: 14px;
                font-size: 0.75rem;
                font-weight: 700;
            }

            .badge-delayed {
                background-color: #fee2e2;
                color: #b91c1c;
                border: 1px solid #fca5a5;
                padding: 4px 12px;
                border-radius: 14px;
                font-size: 0.75rem;
                font-weight: 700;
            }

            .badge-approach {
                background-color: #fef3c7;
                color: #b45309;
                border: 1px solid #fde047;
                padding: 4px 12px;
                border-radius: 14px;
                font-size: 0.75rem;
                font-weight: 700;
            }

            /* Sidebar Custom Styling */
            section[data-testid="stSidebar"] {
                background-color: #0369a1 !important;
                border-right: 2px solid #0284c7;
            }

            section[data-testid="stSidebar"] * {
                color: #ffffff !important;
            }
        </style>
    """, unsafe_allow_html=True)

def render_flightaware_navbar():
    st.markdown("""
        <div class="sky-header">
            <div class="sky-logo">✈️ Sky<span>Metrics</span></div>
            <div class="nav-links">
                <span>Flight Tracking</span>
                <span>Airports & Weather</span>
                <span>ML Predictions</span>
                <span>ETL Pipelines</span>
                <span>AI Insights</span>
            </div>
            <div class="signup-btn">SkyMetrics Pro</div>
        </div>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    """Renders Sky Blue & White banner header for page modules."""
    render_flightaware_navbar()
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 22px 28px; border-radius: 12px; border-left: 6px solid #38bdf8; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.25);">
            <h2 style="margin: 0; color: #ffffff; font-weight: 800; font-size: 1.8rem;">{title}</h2>
            <span style="color: #e0f2fe; font-size: 1rem; font-weight: 500;">{subtitle}</span>
        </div>
    """, unsafe_allow_html=True)
