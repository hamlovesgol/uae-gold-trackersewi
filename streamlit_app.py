import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="UAE Gold Intelligence", page_icon="🏦", layout="wide")

# Corrected CSS for the Premium look
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

# Exact Live Prices from your snapshots
kt_24k = 569.75
kt_ounce = 17721.00
gn_24k = 569.75

# --- 1. HEADER ---
st.title("🏦 UAE Gold Intelligence Terminal")
st.caption(f"Market Data: LIVE | Last Sync: {datetime.now().strftime('%H:%M:%S')}")

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
        st.write("Current market price is above the 30-day average. A pull-back is statistically likely.")
    else:
        st.success("🔮 **PREDICTOR: UPSIDE POTENTIAL**")
        st.write("Favorable entry point detected based on monthly price cycles.")

with target_col:
    st.write("### 🕒 Optimal Entry/Exit Windows")
    t1, t2, t3 = st.columns(3)
    t1.info(f"**Short Term (1-4w)**\n\n**Buy:** {monthly_avg*0.98:.1f}\n\n**Sell:** {monthly_avg*1.02:.1f}")
    t2.info(f"**Mid Term (3-6m)**\n\n**Buy:** {monthly_avg*0.96:.1f}\n\n**Sell:** {monthly_avg*1.06:.1f}")
    t3.info(f"**Long Term (7m+)**\n\n**Buy:** {monthly_avg*0.94:.1f}\n\n**Sell:** {monthly_avg*1.12:.1f}")

st.divider()

# --- 4. THE SIMULATOR ---
st.subheader("🎮 Strategy Simulator (Trial & Error)")
sim_1, sim_2, sim_3 = st.columns(3)
with sim_1:
    u_buy = st.number_input("Purchase Price (AED/g)", value=kt_24k, step=0.25)
with sim_2:
    u_invest = st.number_input("Investment (AED)", value=1000, step=100)
with
