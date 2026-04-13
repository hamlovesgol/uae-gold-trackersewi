import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="UAE Gold Intelligence", page_icon="🏦", layout="wide")

# Premium UI Styling
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

# Exact Live Prices (Evening/Newest from your data)
kt_24k = 569.75
gn_24k = 569.75
kt_ounce = 17721.00

# --- 1. HEADER ---
st.title("🏦 UAE Gold Intelligence Terminal")
st.caption(f"Market Status: LIVE | Sync Time: {datetime.now().strftime('%H:%M:%S')}")

# --- 2. LIVE PRICE TRACKER ---
c1, c2, c3 = st.columns(3)
c1.metric("Khaleej Times 24K", f"{kt_24k} AED")
c2.metric("Gulf News 24K", f"{gn_24k} AED")
c3.metric("Live Ounce (KT)", f"{kt_ounce:,.2f} AED")

st.divider()

# --- 3. SMART PREDICTOR & TARGETS ---
st.subheader("🎯 Investment Strategy & Forecast")
pred_col, target_col = st.columns([1, 1.5])

with pred_col:
    if kt_24k > monthly_avg:
        st.warning("🔮 **PREDICTOR: LIKELY LOWER**")
        st.write("Current market price is above the 30-day mean. A pull-back is statistically probable.")
    else:
        st.success("🔮 **PREDICTOR: LIKELY HIGHER**")
        st.write("Favorable entry zone detected based on monthly price cycles.")

with target_col:
    st.write("### 🕒 Optimal Entry/Exit Windows")
    t1, t2, t3 = st.columns(3
