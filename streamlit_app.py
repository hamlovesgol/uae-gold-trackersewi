import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="UAE Gold Intelligence", page_icon="🏦", layout="wide")

# Corrected Premium CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 32px; color: #f0c05a !important; font-weight: bold; }
    .stAlert { border-radius: 12px; border: 1px solid #f0c05a22; }
    h1, h2, h3 { color: #f0c05a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA CONFIGURATION ---
hist_prices = [
    569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
    563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 
    529.25, 543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 
    600.00, 602.50, 604.75
]
monthly_avg = sum(hist_prices) / len(hist_prices)

# Exact Live Prices (Updated per your newest data)
kt_24k = 569.75
kt_ounce = 17721.00
gn_24k = 569.75

# --- 1. HEADER ---
st.title("🏦 UAE Gold Intelligence Terminal")
st.caption(f"Market Status: LIVE | Last Update: {datetime.now().strftime('%H:%M:%S')}")

# --- 2. LIVE PRICE TRACKER ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Khaleej Times 24K", f"{kt_24k} AED")
with col2:
    st.metric("Gulf News 24K", f"{gn_24k} AED")
with col3:
    st.metric("Gold Ounce (KT)", f"{kt_ounce:,.2f} AED")

st.divider()

# --- 3. SMART PREDICTOR & TARGETS ---
st.subheader("🎯 Investment Strategy & Forecast")
pred_col, target_col = st.columns([1, 1.5])

with pred_col:
    if kt_24k > monthly_avg:
        st.warning("🔮 **PREDICTOR: EXPECTED DROP**")
        st.write("Market price is currently above the 30-day mean. A pull-back is statistically likely.")
    else:
        st.success("🔮 **PREDICTOR: UPSIDE POTENTIAL**")
        st.write("Current rates are favorable compared to the monthly average cycle.")

with target_col:
    st.write("### 🕒 Optimal Entry/Exit Windows")
    t1, t2, t3 = st.columns(3)
    t1.info(f"**Short Term**\n\nBuy: {monthly_avg*0.98:.1f}\n\nSell: {monthly_avg*1.02:.1f}")
    t2.info(f"**Mid Term**\n\nBuy: {monthly_avg*0.96:.1f}\n\nSell: {monthly_avg*1.06:.1f}")
    t3.info(f"**Long Term**\n\nBuy: {monthly_avg*0.94:.1f}\n\nSell: {monthly_avg*1.12:.1f}")

st.divider()

# --- 4. THE SIMULATOR ---
st.subheader("🎮 Strategy Simulator (Trial & Error)")
sim_col1, sim_col2, sim_col3 = st.columns(3)
with sim_col1:
    u_buy = st.number_input("Your Buy Price (AED/g)", value=kt_24k, step=0.1)
with sim_col2:
    u_invest = st.number_input("Total Investment (AED)", value=1000, step=100)
with sim_col3:
    u_future = st.slider("Predicted Sale Price (AED/g)", 450.0, 650.0, kt_24k + 5.0)

# Calculations
grams = u_invest / u_buy
profit = (grams * u_future) - u_invest
roi = (profit / u_invest) * 100

if profit >= 0:
    st.write(f"### 📈 Projected Profit: **{profit:.2f} AED** ({roi:.2f}%)")
else:
    st.write(f"### 📉 Projected Loss: **{abs(profit):.2f} AED** ({roi:.2f}%)")

st.divider()

# --- 5. HISTORICAL TREND ---
st.subheader("📊 24K Performance Trend")
hist_dates = [f"{i} Apr" for i in range(13, 0, -1)] + [f"{i} Mar" for i in range(31, 14, -1)]
df = pd.DataFrame({'Date': hist_dates, 'Price (AED)': hist_prices})
st.line_chart(df.set_index('Date'), color="#f0c05a")

# --- AUTOMATION ---
if "trigger" in st.query_params:
    try:
        requests.post(f"https://ntfy.sh/hamdan_gold_alerts_2026", 
                      data=f"Gold: {kt_24k} AED | Ounce: {kt_ounce} AED".encode('utf-8'))
    except:
        pass
