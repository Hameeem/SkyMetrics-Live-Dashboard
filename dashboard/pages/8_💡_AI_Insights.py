import streamlit as st

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("AI Operational Insights & NLP Intelligence", "Natural language automated summaries, flight disruption diagnostics, and recommended action plans.")

airport_select = st.selectbox("Filter Operational Focus Hub", ["ALL", "LHR", "DEL", "JFK", "HND", "DXB", "ORD"])

insights = api_client.get_ai_insights(airport_select)

st.markdown(f"""
<div class="glass-card">
    <h3 style="color: #38bdf8; margin-top:0;">🤖 AI Executive Intelligence Summary ({insights.get('provider', 'builtin').upper()} Engine)</h3>
    <p style="font-size: 1.1rem; line-height: 1.6; color: #f3f4f6;">
        {insights.get('summary')}
    </p>
    <div style="margin-top: 15px;">
        <b>Operational Risk Status:</b> <span class="badge-approach">{insights.get('risk_status', 'MODERATE')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.subheader("Key Findings & Airspace Insights")
for idx, ins in enumerate(insights.get("insights_list", []), 1):
    st.markdown(f"**{idx}.** {ins}")

st.markdown("<br/>", unsafe_allow_html=True)
st.subheader("Recommended Dispatcher Actions")
for rec in insights.get("recommendations", []):
    st.info(f"🔹 {rec}")
