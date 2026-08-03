import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from dashboard.components.styles import apply_custom_theme, render_header

apply_custom_theme()

st.markdown("""
<style>
    div[data-testid="stMetricLabel"] *, label[data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

render_header("Airport & Airline Operations Analysis Dashboard", "Filter live operational analytics by Airport Hub, Time Horizon (Today, Week, Month, Year), Airline On-Time %, Takeoffs/Landings, and Side-by-Side Airport Comparison across Indian and Global Hubs.")

# Master Dataset: All Major Indian Airports + Famous International Airport per Country
all_airports_master = [
    # --- ALL HUB OVERVIEW ---
    {"iata": "ALL", "name": "ALL - All Indian Airspace Hubs", "city": "All Cities", "country": "India", "takeoffs": 420},
    
    # --- INDIA (ALL MAJOR & REGIONAL AIRPORTS) ---
    {"iata": "DEL", "name": "DEL - Indira Gandhi Int'l (Delhi)", "city": "New Delhi", "country": "India", "takeoffs": 142},
    {"iata": "BOM", "name": "BOM - Chhatrapati Shivaji Maharaj Int'l (Mumbai)", "city": "Mumbai", "country": "India", "takeoffs": 98},
    {"iata": "BLR", "name": "BLR - Kempegowda Int'l (Bengaluru)", "city": "Bengaluru", "country": "India", "takeoffs": 75},
    {"iata": "MAA", "name": "MAA - Chennai Int'l (Chennai)", "city": "Chennai", "country": "India", "takeoffs": 62},
    {"iata": "HYD", "name": "HYD - Rajiv Gandhi Int'l (Hyderabad)", "city": "Hyderabad", "country": "India", "takeoffs": 54},
    {"iata": "CCU", "name": "CCU - Netaji Subhash Chandra Bose Int'l (Kolkata)", "city": "Kolkata", "country": "India", "takeoffs": 48},
    {"iata": "AMD", "name": "AMD - Sardar Vallabhbhai Patel Int'l (Ahmedabad)", "city": "Ahmedabad", "country": "India", "takeoffs": 42},
    {"iata": "COK", "name": "COK - Cochin Int'l (Kochi)", "city": "Kochi", "country": "India", "takeoffs": 40},
    {"iata": "GOI", "name": "GOI - Dabolim Airport (Goa)", "city": "Goa", "country": "India", "takeoffs": 38},
    {"iata": "GOX", "name": "GOX - Manohar Int'l (Mopa, Goa)", "city": "Mopa Goa", "country": "India", "takeoffs": 28},
    {"iata": "PNQ", "name": "PNQ - Pune Airport (Pune)", "city": "Pune", "country": "India", "takeoffs": 35},
    {"iata": "LKO", "name": "LKO - Chaudhary Charan Singh Int'l (Lucknow)", "city": "Lucknow", "country": "India", "takeoffs": 32},
    {"iata": "JAI", "name": "JAI - Jaipur Int'l (Jaipur)", "city": "Jaipur", "country": "India", "takeoffs": 30},
    {"iata": "SXR", "name": "SXR - Sheikh ul-Alam Int'l (Srinagar)", "city": "Srinagar", "country": "India", "takeoffs": 28},
    {"iata": "GAU", "name": "GAU - Lokpriya Gopinath Bordoloi Int'l (Guwahati)", "city": "Guwahati", "country": "India", "takeoffs": 26},
    {"iata": "IXC", "name": "IXC - Shaheed Bhagat Singh Int'l (Chandigarh)", "city": "Chandigarh", "country": "India", "takeoffs": 25},
    {"iata": "PAT", "name": "PAT - Jayprakash Narayan Airport (Patna)", "city": "Patna", "country": "India", "takeoffs": 24},
    {"iata": "BBI", "name": "BBI - Biju Patnaik Int'l (Bhubaneswar)", "city": "Bhubaneswar", "country": "India", "takeoffs": 23},
    {"iata": "ATQ", "name": "ATQ - Sri Guru Ram Dass Jee Int'l (Amritsar)", "city": "Amritsar", "country": "India", "takeoffs": 22},
    {"iata": "VTZ", "name": "VTZ - Visakhapatnam Int'l (Visakhapatnam)", "city": "Visakhapatnam", "country": "India", "takeoffs": 21},
    {"iata": "TRV", "name": "TRV - Trivandrum Int'l (Thiruvananthapuram)", "city": "Thiruvananthapuram", "country": "India", "takeoffs": 20},
    {"iata": "CJB", "name": "CJB - Coimbatore Int'l (Coimbatore)", "city": "Coimbatore", "country": "India", "takeoffs": 19},
    {"iata": "TRZ", "name": "TRZ - Tiruchirappalli Int'l (Trichy)", "city": "Trichy", "country": "India", "takeoffs": 18},
    {"iata": "IXM", "name": "IXM - Madurai Airport (Madurai)", "city": "Madurai", "country": "India", "takeoffs": 16},
    {"iata": "IXB", "name": "IXB - Bagdogra Airport (Siliguri/Darjeeling)", "city": "Bagdogra", "country": "India", "takeoffs": 18},
    {"iata": "VNS", "name": "VNS - Lal Bahadur Shastri Int'l (Varanasi)", "city": "Varanasi", "country": "India", "takeoffs": 19},
    {"iata": "IDR", "name": "IDR - Devi Ahilya Bai Holkar Airport (Indore)", "city": "Indore", "country": "India", "takeoffs": 21},
    {"iata": "BHO", "name": "BHO - Raja Bhoj Airport (Bhopal)", "city": "Bhopal", "country": "India", "takeoffs": 15},
    {"iata": "IXR", "name": "IXR - Birsa Munda Airport (Ranchi)", "city": "Ranchi", "country": "India", "takeoffs": 17},
    {"iata": "RPR", "name": "RPR - Swami Vivekananda Airport (Raipur)", "city": "Raipur", "country": "India", "takeoffs": 16},
    {"iata": "DHM", "name": "DHM - Kangra Gaggal Airport (Dharamshala)", "city": "Dharamshala", "country": "India", "takeoffs": 14},
    {"iata": "IXJ", "name": "IXJ - Jammu Airport (Jammu)", "city": "Jammu", "country": "India", "takeoffs": 18},
    {"iata": "LEH", "name": "LEH - Kushok Bakula Rimpochee Airport (Leh)", "city": "Leh", "country": "India", "takeoffs": 12},
    {"iata": "IXA", "name": "IXA - Maharaja Bir Bikram Airport (Agartala)", "city": "Agartala", "country": "India", "takeoffs": 14},
    {"iata": "IMF", "name": "IMF - Imphal International Airport (Imphal)", "city": "Imphal", "country": "India", "takeoffs": 13},

    # --- FAMOUS INTERNATIONAL AIRPORTS (PER COUNTRY WORLDWIDE) ---
    {"iata": "DXB", "name": "DXB - Dubai International (United Arab Emirates)", "city": "Dubai", "country": "UAE", "takeoffs": 185},
    {"iata": "LHR", "name": "LHR - London Heathrow Airport (United Kingdom)", "city": "London", "country": "UK", "takeoffs": 160},
    {"iata": "JFK", "name": "JFK - John F. Kennedy Int'l (United States)", "city": "New York", "country": "USA", "takeoffs": 175},
    {"iata": "LAX", "name": "LAX - Los Angeles International (United States)", "city": "Los Angeles", "country": "USA", "takeoffs": 165},
    {"iata": "SIN", "name": "SIN - Singapore Changi Airport (Singapore)", "city": "Singapore", "country": "Singapore", "takeoffs": 150},
    {"iata": "HND", "name": "HND - Tokyo Haneda Airport (Japan)", "city": "Tokyo", "country": "Japan", "takeoffs": 170},
    {"iata": "CDG", "name": "CDG - Paris Charles de Gaulle (France)", "city": "Paris", "country": "France", "takeoffs": 155},
    {"iata": "FRA", "name": "FRA - Frankfurt Airport (Germany)", "city": "Frankfurt", "country": "Germany", "takeoffs": 148},
    {"iata": "AMS", "name": "AMS - Amsterdam Schiphol (Netherlands)", "city": "Amsterdam", "country": "Netherlands", "takeoffs": 145},
    {"iata": "DOH", "name": "DOH - Hamad International Airport (Qatar)", "city": "Doha", "country": "Qatar", "takeoffs": 162},
    {"iata": "SYD", "name": "SYD - Sydney Kingsford Smith (Australia)", "city": "Sydney", "country": "Australia", "takeoffs": 130},
    {"iata": "YYZ", "name": "YYZ - Toronto Pearson Int'l (Canada)", "city": "Toronto", "country": "Canada", "takeoffs": 138},
    {"iata": "BKK", "name": "BKK - Suvarnabhumi Airport (Thailand)", "city": "Bangkok", "country": "Thailand", "takeoffs": 142},
    {"iata": "KUL", "name": "KUL - Kuala Lumpur Int'l (Malaysia)", "city": "Kuala Lumpur", "country": "Malaysia", "takeoffs": 125},
    {"iata": "PEK", "name": "PEK - Beijing Capital Int'l (China)", "city": "Beijing", "country": "China", "takeoffs": 180},
    {"iata": "HKG", "name": "HKG - Hong Kong International (Hong Kong)", "city": "Hong Kong", "country": "Hong Kong", "takeoffs": 140},
    {"iata": "IST", "name": "IST - Istanbul Airport (Turkey)", "city": "Istanbul", "country": "Turkey", "takeoffs": 168},
    {"iata": "JED", "name": "JED - King Abdulaziz Int'l (Saudi Arabia)", "city": "Jeddah", "country": "Saudi Arabia", "takeoffs": 135},
    {"iata": "MAD", "name": "MAD - Madrid-Barajas Airport (Spain)", "city": "Madrid", "country": "Spain", "takeoffs": 132},
    {"iata": "FCO", "name": "FCO - Rome Leonardo da Vinci (Italy)", "city": "Rome", "country": "Italy", "takeoffs": 128},
    {"iata": "ICN", "name": "ICN - Incheon International (South Korea)", "city": "Seoul", "country": "South Korea", "takeoffs": 152},
    {"iata": "CGK", "name": "CGK - Soekarno-Hatta Int'l (Indonesia)", "city": "Jakarta", "country": "Indonesia", "takeoffs": 120},
    {"iata": "JNB", "name": "JNB - O.R. Tambo Int'l (South Africa)", "city": "Johannesburg", "country": "South Africa", "takeoffs": 95},
    {"iata": "GRU", "name": "GRU - São Paulo/Guarulhos Int'l (Brazil)", "city": "São Paulo", "country": "Brazil", "takeoffs": 110},
    {"iata": "MEX", "name": "MEX - Mexico City International (Mexico)", "city": "Mexico City", "country": "Mexico", "takeoffs": 115},
    {"iata": "CAI", "name": "CAI - Cairo International Airport (Egypt)", "city": "Cairo", "country": "Egypt", "takeoffs": 90}
]

# Airport Search Box & Filter System
st.markdown("### 🔍 Global & Indian Airport Operations Search Engine")
c_srch1, c_srch2, c_srch3 = st.columns([5, 4, 3])

with c_srch1:
    search_term = st.text_input("🔍 Search Airport (by Code, City, or Country)", placeholder="Type SXR, DHM, Delhi, Srinagar, Goa, Tokyo, Dubai, London, New York...").strip().upper()

matching_airports = [ap["name"] for ap in all_airports_master if not search_term or search_term in ap["iata"] or search_term in ap["name"].upper() or search_term in ap["city"].upper() or search_term in ap["country"].upper()]

if not matching_airports:
    matching_airports = [ap["name"] for ap in all_airports_master]

with c_srch2:
    selected_primary = st.selectbox("📍 Select Primary Airport Hub", matching_airports, index=0)

with c_srch3:
    timeframe = st.selectbox("📅 Timeframe Horizon", ["Today (24 Hours)", "Past 7 Days (Week)", "Past 30 Days (Month)", "Past 365 Days (Year)"])

# Optional Side-by-Side Airport Comparison Toggle
st.markdown("---")
enable_compare = st.checkbox("⚔️ Enable Side-by-Side Airport Comparison")

if enable_compare:
    c_cmp1, c_cmp2 = st.columns(2)
    with c_cmp1:
        st.info(f"**Primary Target:** {selected_primary}")
    with c_cmp2:
        selected_secondary = st.selectbox("📍 Select Comparison Airport", [ap["name"] for ap in all_airports_master if ap["name"] != selected_primary], index=1)

st.markdown("<br/>", unsafe_allow_html=True)

# Helper function to get stats for an airport name
def get_ap_stats(ap_fullname, tf_name):
    mult = 1 if "Today" in tf_name else (7 if "Week" in tf_name else (30 if "Month" in tf_name else 365))
    ap_entry = next((ap for ap in all_airports_master if ap["name"] == ap_fullname), all_airports_master[0])
    code = ap_entry["iata"]
    base_t = ap_entry["takeoffs"]
    
    takeoffs = base_t * mult
    landings = int(base_t * 0.96) * mult
    delayed = int(base_t * 0.12) * mult
    ontime_rate = 88.5 if code == "BLR" else (87.2 if code == "DEL" else (84.1 if code == "SXR" else 86.4))
    
    return {
        "code": code,
        "name": ap_fullname,
        "takeoffs": takeoffs,
        "landings": landings,
        "delayed": delayed,
        "ontime_rate": ontime_rate,
        "base_t": base_t,
        "mult": mult
    }

p_stats = get_ap_stats(selected_primary, timeframe)

if not enable_compare:
    # Single Airport Analytics Overview
    k1, k2, k3, k4 = st.columns(4)
    dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    b_t = p_stats["base_t"]

    with k1:
        st.metric("🛫 Takeoffs / Departures", f"{p_stats['takeoffs']:,}", f"+{int(p_stats['mult']*4.2)} vs prev")
        fig_k1 = go.Figure(data=go.Scatter(x=dates, y=[b_t - 5, b_t + 8, b_t - 2, b_t + 12, b_t - 4, b_t + 6, b_t], mode='lines', line=dict(color="#1E88E5", width=3)))
        fig_k1.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_k1, use_container_width=True)

    with k2:
        st.metric("🛬 Landings / Arrivals", f"{p_stats['landings']:,}", f"+{int(p_stats['mult']*3.8)} vs prev")
        fig_k2 = go.Figure(data=go.Scatter(x=dates, y=[b_t - 6, b_t + 5, b_t - 4, b_t + 10, b_t - 2, b_t + 4, b_t - 2], mode='lines', line=dict(color="#0284C7", width=3)))
        fig_k2.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_k2, use_container_width=True)

    with k3:
        st.metric("🛑 Delayed Flights (>15m)", f"{p_stats['delayed']:,}", f"-{int(p_stats['mult']*1.1)} vs prev", delta_color="inverse")
        fig_k3 = go.Figure(data=go.Scatter(x=dates, y=[int(b_t*0.18), int(b_t*0.14), int(b_t*0.15), int(b_t*0.11), int(b_t*0.13), int(b_t*0.10), int(b_t*0.12)], mode='lines', line=dict(color="#0F172A", width=3)))
        fig_k3.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_k3, use_container_width=True)

    with k4:
        st.metric("🎯 On-Time Arrival Rate", f"{p_stats['ontime_rate']:.1f}%", "+1.4% Target")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=p_stats['ontime_rate'],
            gauge={'axis': {'range': [0, 100], 'tickcolor': "#0F172A"}, 'bar': {'color': "#1E88E5"}, 'steps': [{'range': [0, 75], 'color': "#F8FAFC"}, {'range': [75, 85], 'color': "#E2E8F0"}, {'range': [85, 100], 'color': "#BAE6FD"}]}
        ))
        fig_gauge.update_layout(height=130, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#FFFFFF", font=dict(color="#0F172A"))
        st.plotly_chart(fig_gauge, use_container_width=True)

else:
    # Side-by-Side Comparison Layout
    s_stats = get_ap_stats(selected_secondary, timeframe)
    st.subheader(f"⚔️ Operational Comparison: {p_stats['code']} vs {s_stats['code']}")
    
    col_ap1, col_ap2 = st.columns(2)
    with col_ap1:
        st.markdown(f"### 📍 {p_stats['name']}")
        m1, m2 = st.columns(2)
        m1.metric("Departures", f"{p_stats['takeoffs']:,}")
        m2.metric("On-Time Rate", f"{p_stats['ontime_rate']:.1f}%")
        st.metric("Delays (>15m)", f"{p_stats['delayed']:,}")

    with col_ap2:
        st.markdown(f"### 📍 {s_stats['name']}")
        m3, m4 = st.columns(2)
        m3.metric("Departures", f"{s_stats['takeoffs']:,}")
        m4.metric("On-Time Rate", f"{s_stats['ontime_rate']:.1f}%")
        st.metric("Delays (>15m)", f"{s_stats['delayed']:,}")

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("📊 Comparative Departure Volume Bar Chart")
    fig_cmp_bar = go.Figure(data=[
        go.Bar(name=p_stats['code'], x=["Takeoffs", "Landings", "Delays"], y=[p_stats['takeoffs'], p_stats['landings'], p_stats['delayed']], marker_color="#1E88E5"),
        go.Bar(name=s_stats['code'], x=["Takeoffs", "Landings", "Delays"], y=[s_stats['takeoffs'], s_stats['landings'], s_stats['delayed']], marker_color="#0F172A")
    ])
    fig_cmp_bar.update_layout(barmode='group', paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#0F172A"))
    st.plotly_chart(fig_cmp_bar, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
col_left, col_mid = st.columns([5, 5])

with col_left:
    st.subheader("✈️ Airline On-Time Performance & Delays")
    df_airlines = pd.DataFrame([
        {"Airline": "IndiGo", "Total Flights": int(p_stats['takeoffs']*0.48), "On-Time %": "91.4%", "Avg Delay": "11.2 min", "Status": "OPTIMAL"},
        {"Airline": "Air India", "Total Flights": int(p_stats['takeoffs']*0.26), "On-Time %": "84.8%", "Avg Delay": "22.5 min", "Status": "NOMINAL"},
        {"Airline": "Vistara", "Total Flights": int(p_stats['takeoffs']*0.14), "On-Time %": "89.2%", "Avg Delay": "14.1 min", "Status": "GOOD"},
        {"Airline": "Akasa Air", "Total Flights": int(p_stats['takeoffs']*0.07), "On-Time %": "88.6%", "Avg Delay": "15.0 min", "Status": "GOOD"},
        {"Airline": "SpiceJet", "Total Flights": int(p_stats['takeoffs']*0.05), "On-Time %": "81.2%", "Avg Delay": "26.8 min", "Status": "ATTENTION"}
    ])
    st.dataframe(df_airlines, use_container_width=True, hide_index=True)

with col_mid:
    st.subheader("📍 Top Route Corridor Traffic Density")
    df_routes = pd.DataFrame([
        {"Route Corridor": f"{p_stats['code']} ➔ BOM (Mumbai)", "Daily Flights": int(p_stats['takeoffs']*0.22), "Share %": "22.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ BLR (Bengaluru)", "Daily Flights": int(p_stats['takeoffs']*0.18), "Share %": "18.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ SXR (Srinagar)", "Daily Flights": int(p_stats['takeoffs']*0.12), "Share %": "12.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ MAA (Chennai)", "Daily Flights": int(p_stats['takeoffs']*0.10), "Share %": "10.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ DHM (Dharamshala)", "Daily Flights": int(p_stats['takeoffs']*0.06), "Share %": "6.0%"}
    ])
    st.dataframe(df_routes, use_container_width=True, hide_index=True)
