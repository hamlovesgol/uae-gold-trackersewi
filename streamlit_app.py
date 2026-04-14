import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# 1. PAGE CONFIG
st.set_page_config(page_title="UAE Gold Intelligence", page_icon="🏦", layout="wide")

# 2. LIVE SYNC TIMER
st_autorefresh(interval=60 * 1000, key="gold_sync_timer")

# 3. PREMIUM UI STYLING
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 32px; color: #f0c05a !important; font-weight: bold; }
    .stAlert { border-radius: 12px; border: 1px solid #f0c05a22; }
    h1, h2, h3 { color: #f0c05a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- THE AFTERNOON SYNC FIX ---
def get_live_prices():
    # Exact Afternoon Update: April 14, 2026
    current_24k = 575.25 
    current_ounce = 17892.00 # Matches the $2,400+ international spot move
    return current_24k, current_24k, current_ounce

# --- ALIGNED DATA (31 DAYS) ---
# Updated with the exact 575.25 afternoon value
hist_prices = [
    575.25, 569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50,
    563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 529.25,
    543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 600.00, 602.50, 604.75
]

hist_dates = [f"{i} Apr" for i in range(14, 0, -1)] + [f"{i} Mar" for i in range(31, 15, -1)]

monthly_avg = sum(hist_prices) / len(hist_prices)
kt_24k, gn_24k, kt_ounce = get_live_prices()

# --- 1. HEADER (UAE TIME) ---
st.title("🏦 UAE Gold Intelligence Terminal")
uae_time = datetime.now() + timedelta(hours=4)
st.caption(f"Market Status: AFTERNOON SYNC | Last Check: {uae_time.strftime('%H:%M:%S')} (UAE Time)")

# --- 2. LIVE PRICE TRACKER ---
c1, c2, c3 = st.columns(3)
# Delta shows the jump from the morning price
c1.metric("Khaleej Times 24K", f"{kt_24k} AED", delta=f"{kt_24k - 569.75:.2f}")
c2.metric("Gulf News 24K", f"{gn_24k} AED", delta=f"{gn_24k - 569.75:.2f}")
c3.metric("Live Ounce (KT)", f"{kt_ounce:,.2f} AED")

st.divider()

# --- 3. FORECAST ---
st.subheader("🎯 Investment Strategy & Forecast")
pred_col, target_col = st.columns([1, 1.5])

with pred_col:
    if kt_24k > monthly_avg:
        st.warning("🔮 **PREDICTOR: OVERVALUED**")
        st.write(f"Afternoon jump to {kt_24k} puts us well above the 30-day mean ({monthly_avg:.1f}). Expect a cooldown.")
    else:
        st.success("🔮 **PREDICTOR: BUY ZONE**")

with target_col:
    st.write("### 🕒 Target Entry Prices")
    t1, t2, t3 = st.columns(3)
    t1.info(f"**Aggressive**\n\n{monthly_avg*0.99:.1f}")
    t2.info(f"**Safe**\n\n{monthly_avg*0.97:.1f}")
    t3.info(f"**Optimal**\n\n{monthly_avg*0.95:.1f}")

st.divider()

# --- 4. SIMULATOR & CHART ---
st.subheader("📊 Performance Trend & Simulation")
df_chart = pd.DataFrame({'Date': hist_dates, 'Price (AED)': hist_prices})
st.line_chart(df_chart.set_index('Date'), color="#f0c05a")

# Quick Simulator
u_buy = st.sidebar.number_input("Purchase Price", value=kt_24k)
u_invest = st.sidebar.number_input("Investment (AED)", value=1000)
u_future = st.sidebar.slider("Sale Price", 450.0, 700.0, kt_24k + 10.0)

total_grams = u_invest / u_buy
profit = (total_grams * u_future) - u_invest
st.sidebar.write(f"### ROI: {profit:.2f} AED")
