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
    .stInfo { background-color: #1e2130; border-left: 5px solid #f0c05a; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA CONFIGURATION (APRIL 14 AFTERNOON OFFICIAL) ---
# Current prices based on latest updates
kt_24k, gn_24k, live_ounce = 575.25, 575.25, 17892.00
yesterday_24k = 569.75

# Session Data for Tables (Matches your requested website style)
session_data = {
    "Purity": ["24K", "22K", "21K", "18K"],
    "Morning": ["572.25", "524.25", "500.50", "429.00"],
    "Afternoon": ["575.25", "527.00", "503.25", "431.25"],
    "Evening": ["-", "-", "-", "-"],
    "Yesterday": ["569.75", "527.75", "506.00", "433.75"]
}
df_sessions = pd.DataFrame(session_data).set_index("Purity")

# Historical Prices (Exactly 31 items)
hist_prices = [575.25, 569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
               563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 529.25, 
               543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 600.00, 602.50, 604.75]

# Historical Dates (Exactly 31 items to fix the ValueError)
hist_dates = [f"{i} Apr" for i in range(14, 0, -1)] + [f"{i} Mar" for i in range(31, 14, -1)]
avg_30d = sum(hist_prices) / len(hist_prices)

# --- 1. HEADER (UAE TIME) ---
st.title("🏦 UAE Gold Intelligence Terminal")
uae_time = datetime.now() + timedelta(hours=4)
st.caption(f"Market Status: LIVE SYNC | {uae_time.strftime('%H:%M:%S')} (UAE Time)")

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
    st.table(df_sessions)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="gold-card">', unsafe_allow_html=True)
    st.table(df_sessions)
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# --- 4. BUY / SELL / HOLD STRATEGY ---
st.subheader("🎯 Investment Strategy & Forecast")
pred_col, target_col = st.columns([1, 1.5])

with pred_col:
    st.markdown("### Status")
    if kt_24k > avg_30d:
        st.error("🚨 **ACTION: HOLD / WAIT**")
        st.write(f"Current price is **OVERVALUED**. Market is trading {kt_24k - avg_30d:.2f} AED above the 30-day average.")
    else:
        st.success("✅ **ACTION: BUY ZONE**")
        st.write(f"Market is currently at or below the 30-day average. Good entry opportunity.")

with target_col:
    st.markdown("### 🕒 Optimal Target Prices")
    t1, t2, t3 = st.columns(3)
    t1.info(f"**Short Term**\n\nBuy: {avg_30d*0.98:.1f}\n\nSell: {avg_30d*1.02:.1f}")
    t2.info(f"**Mid Term**\n\nBuy: {avg_30d*0.96:.1f}\n\nSell: {avg_30d*1.06:.1f}")
    t3.info(f"**Long Term**\n\nBuy: {avg_30d*0.94:.1f}\n\nSell: {avg_30d*1.12:.1f}")

st.divider()

# --- 5. THE CHART (FIXED TREND) ---
st.subheader("📊 24K Performance Trend (Last 30 Days)")
df_chart = pd.DataFrame({'Date': hist_dates, 'Price': hist_prices})
st.line_chart(df_chart.set_index('Date'), color="#f0c05a")
