import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 1. PAGE CONFIG
st.set_page_config(page_title="UAE Gold Intelligence", page_icon="🏦", layout="wide")
st_autorefresh(interval=60 * 1000, key="gold_sync_timer")

# 2. STYLING
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 30px; color: #f0c05a !important; }
    .gold-card { padding: 20px; border: 1px solid #f0c05a44; border-radius: 10px; background: #1a1c24; margin-bottom: 20px; }
    h2, h3 { color: #f0c05a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- THE DATA (APRIL 14 AFTERNOON UPDATE) ---
# Ounce is updated to 17,892.00 to match the 24K price of 575.25
kt_24k, gn_24k, live_ounce = 575.25, 575.25, 17892.00
yesterday_24k = 569.75

# Session Data for Tables
session_data = {
    "Purity": ["24K", "22K", "21K", "18K"],
    "Morning": ["575.25", "532.50", "510.75", "437.75"],
    "Afternoon": ["575.25", "532.50", "510.75", "437.75"],
    "Evening": ["-", "-", "-", "-"],
    "Yesterday": ["569.75", "527.75", "506.00", "433.75"]
}
df_sessions = pd.DataFrame(session_data)

# --- 1. HEADER ---
st.title("🏦 UAE Gold Intelligence Terminal")
uae_time = datetime.now() + timedelta(hours=4)
st.caption(f"Market Status: AFTERNOON SYNC | {uae_time.strftime('%H:%M:%S')} (UAE Time)")

# --- 2. MAIN METRICS ---
m1, m2, m3 = st.columns(3)
m1.metric("Khaleej Times 24K", f"{kt_24k} AED", delta=f"{kt_24k - yesterday_24k:.2f}")
m2.metric("Gulf News 24K", f"{gn_24k} AED", delta=f"{gn_24k - yesterday_24k:.2f}")
m3.metric("Live Ounce (Price/oz)", f"{live_ounce:,.2f} AED", delta="171.00")

st.divider()

# --- 3. DUAL WEBSITE TABLES ---
st.subheader("🗓️ Daily Session Comparison")
tab1, tab2 = st.tabs(["📊 Khaleej Times Sessions", "📊 Gulf News Sessions"])

with tab1:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.write("### KT Official Rates (AED/g)")
    st.table(df_sessions.set_index("Purity"))
    st.caption("Khaleej Times typically updates at 8:00 AM, 12:00 PM, and 6:00 PM.")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.write("### GN Official Rates (AED/g)")
    # Re-displaying for the second website as requested
    st.table(df_sessions.set_index("Purity"))
    st.caption("Gulf News data is sourced from the Dubai Gold & Jewellery Group (DGJG).")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. PREDICTOR & TREND (Simplified for Scannability) ---
st.divider()
hist_prices = [575.25, 569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
               563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 529.25, 
               543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 600.00, 602.50, 604.75]
hist_dates = [f"{i} Apr" for i in range(14, 0, -1)] + [f"{i} Mar" for i in range(31, 15, -1)]

col_left, col_right = st.columns([1, 2])
with col_left:
    st.subheader("🔮 Price Predictor")
    avg = sum(hist_prices) / len(hist_prices)
    if kt_24k > avg:
        st.error(f"**OVERVALUED**\n\nCurrent: {kt_24k}\n\nAvg: {avg:.1f}")
    else:
        st.success("**GOOD ENTRY**")

with col_right:
    st.subheader("📈 30-Day Trend")
    df_chart = pd.DataFrame({'Date': hist_dates, 'Price': hist_prices})
    st.line_chart(df_chart.set_index('Date'), color="#f0c05a")
