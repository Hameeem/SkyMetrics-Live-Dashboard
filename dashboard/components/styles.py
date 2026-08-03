import streamlit as st

def apply_custom_theme():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        
        .stApp {
            background-color: #F8FAFC !important;
            color: #0F172A !important;
        }

        /* Ensure all labels, metric titles, and text in main body are crisp dark black */
        section.main [data-testid="stMetricLabel"] *, 
        section.main [data-testid="stWidgetLabel"] *, 
        section.main label, 
        section.main p, 
        section.main span, 
        section.main h1, 
        section.main h2, 
        section.main h3, 
        section.main h4,
        div[data-testid="stMetricLabel"] {
            color: #0F172A !important;
            font-weight: 800 !important;
        }

        div[data-testid="stMetricValue"] * {
            color: #0F172A !important;
            font-weight: 900 !important;
        }

        /* Hero Card */
        .hero-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 20px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -5px rgba(15, 23, 42, 0.05);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .brand-title {
            font-size: 3.4rem;
            font-weight: 900;
            color: #0F172A;
            margin: 0;
            line-height: 1;
            letter-spacing: -1px;
        }

        .brand-title span {
            color: #1E88E5;
            font-weight: 900;
        }

        .brand-sub {
            font-size: 1.15rem;
            font-weight: 800;
            color: #1E88E5;
            margin-top: 4px;
        }

        .brand-desc {
            font-size: 0.95rem;
            color: #475569;
            margin-top: 2px;
        }

        .radar-badge {
            background: #0F172A;
            border: 2px solid #1E88E5;
            color: #FFFFFF !important;
            font-weight: 800;
            padding: 10px 22px;
            border-radius: 16px;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            box-shadow: 0 0 14px rgba(30, 136, 229, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .green-dot {
            height: 10px;
            width: 10px;
            background-color: #1E88E5;
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px #1E88E5;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0F172A 0%, #1E88E5 100%) !important;
        }

        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header(title: str = "Flight Operations Command Center", subtitle: str = "Real-Time Aviation Intelligence Platform • All-India Airspace Control Sector"):
    st.markdown(f"""
    <div class="hero-card">
        <div>
            <h1 class="brand-title">Sky<span>Metrics</span></h1>
            <div class="brand-sub">{title}</div>
            <div class="brand-desc">{subtitle}</div>
        </div>
        <div class="radar-badge">
            <span class="green-dot"></span> LIVE RADAR ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)
