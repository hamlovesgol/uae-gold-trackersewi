import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 1. PAGE CONFIG & AUTO-REFRESH
st.set_page_config(page_title="UAE Gold Intelligence", page_icon="🏦", layout="wide")
st_autorefresh(interval=60 * 1000, key="gold_sync_timer")

# 2. PREMIUM UI STYLING
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 30px; color: #f0c05a !important; font-weight: bold; }
    .gold-card { padding: 15px; border: 1px solid #f0c05a44; border-radius: 10px; background: #1a1c24; }
    h1, h2, h3 { color: #f0c05a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- THE DATA (APRIL 14 AFTERNOON OFFICIAL) ---
# Ounce is exactly 17,892.00 to match the 24K afternoon price of 575.25
kt_24k, gn_24k, live_ounce = 575.25, 575.25, 17892.00
yesterday_24k = 569.75

# Session Data for Tables (Mirroring your screenshots)
session_data = {
    "Purity": ["24K", "22K", "21K", "18K"],
    "Morning": ["572.25", "524.25", "500.50", "429.00"],
    "Afternoon": ["575.25", "527.00", "503.25", "431.25"],
    "Evening": ["-", "-", "-", "-"],
    "Yesterday": ["569.75", "527.75", "506.00", "433.75"]
}
df_sessions = pd.DataFrame(session_data).set_index("Purity")

# --- 1. HEADER (UAE TIME) ---
st.title("🏦 UAE Gold Intelligence Terminal")
uae_time = datetime.now() + timedelta(hours=4)
st.caption(f"Market Status: AFTERNOON SYNC | {uae_time.strftime('%H:%M:%S')} (UAE Time)")

# --- 2. LIVE METRICS ---
m1, m2, m3 = st.columns(3)
m1.metric("Khaleej Times 24K", f"{kt_24k} AED", delta=f"{kt_24k - yesterday_24k:.2f}")
m2.metric("Gulf News 24K", f"{gn_24k} AED", delta=f"{gn_24k - yesterday_24k:.2f}")
m3.metric("Live Ounce (Price/oz)", f"{live_ounce:,.2f} AED", delta=f"{live_ounce - 17721:.0f}")

st.divider()

# --- 3. DUAL WEBSITE TABLES ---
st.subheader("🗓️ Daily Session Comparison")
tab1, tab2 = st.tabs(["📊 Khaleej Times Official", "📊 Gulf News Official"])

with tab1:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.write("### KT Afternoon Updated Rates (AED/g)")
    st.table(df_sessions)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.write("### GN Official DGJG Rates (AED/g)")
    st.table(df_sessions)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PREDICTOR & FIXED TREND CHART ---
st.divider()
c_left, c_right = st.columns([1, 2])

# Price History (Must be exactly 31 items)
hist_prices = [575.25, 569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
               563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 529.25, 
               543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 600.00, 602.50, 604.75]

# Date History (Must be exactly 31 items)
hist_dates = [f"{i} Apr" for i in range(14, 0, -1)] + [f"{i} Mar" for i in range(31, 14, -1)]

with c_left:
    st.subheader("🔮 Price Predictor")
    avg_price = sum(hist_prices) / len(hist_prices)
    if kt_24k > avg_price:
        st.error(f"**OVERVALUED**\n\nCurrent: {kt_24k}\n\n30D Avg: {avg_price:.1f}")
    else:
        st.success("**GOOD ENTRY ZONE**")

with c_right:
    st.subheader("📈 30-Day Trend")
    # THE FIX: Both lists are now exactly 31 items long
    df_chart = pd.DataFrame({'Date': hist_dates, 'Price': hist_prices})
    st.line_chart(df_chart.set_index('Date'), color="#f0c05a")
