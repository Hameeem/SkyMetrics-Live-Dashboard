import streamlit as st

def apply_custom_theme():
    """Applies modern dark enterprise glassmorphism CSS theme to Streamlit app."""
    st.markdown("""
        <style>
            /* Global Dark Theme & Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }

            .stApp {
                background: linear-gradient(135deg, #0b0f19 0%, #111827 50%, #0f172a 100%);
                color: #f3f4f6;
            }

            /* Glassmorphism Container Card */
            .glass-card {
                background: rgba(17, 24, 39, 0.7);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
                transition: transform 0.2s ease, border-color 0.2s ease;
            }

            .glass-card:hover {
                border-color: rgba(59, 130, 246, 0.4);
                transform: translateY(-2px);
            }

            /* Metric Display Card */
            .metric-card {
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 10px;
                padding: 16px 20px;
                text-align: center;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            }

            .metric-card .value {
                font-size: 2rem;
                font-weight: 700;
                color: #38bdf8;
                letter-spacing: -0.5px;
            }

            .metric-card .label {
                font-size: 0.85rem;
                color: #9ca3af;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 4px;
            }

            /* Status Badges */
            .badge-enroute {
                background-color: rgba(16, 185, 129, 0.2);
                color: #34d399;
                border: 1px solid rgba(16, 185, 129, 0.4);
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
                background-color: #0d1322 !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }

            /* Custom Header Badge */
            .header-banner {
                background: linear-gradient(90deg, #1e3a8a 0%, #0369a1 50%, #0d9488 100%);
                padding: 24px;
                border-radius: 14px;
                color: white;
                margin-bottom: 25px;
                box-shadow: 0 10px 25px -5px rgba(3, 105, 161, 0.4);
            }
        </style>
    """, unsafe_allow_html=True)

def render_header(title: str, subtitle: str):
    st.markdown(f"""
        <div class="header-banner">
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; color: #ffffff;">{title}</h1>
            <p style="margin: 6px 0 0 0; font-size: 1.05rem; opacity: 0.9;">{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)
