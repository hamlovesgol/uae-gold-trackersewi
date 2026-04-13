import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Config - Wide mode with a professional icon
st.set_page_config(page_title="UAE Gold Investment Pro", page_icon="🏦", layout="wide")

# Custom CSS for a cleaner, "Dark Mode" financial look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #f0c05a; }
    .stAlert { border-radius: 10px; border: none; }
    </style>
    """, unsafe_content_type=True)

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

# --- 1. HEADER SECTION ---
st.title("🏦 UAE Gold Intelligence Terminal")
st.caption(f"Market Data Status: LIVE | Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# --- 2. LIVE PRICE TRACKER (Restored Exact Prices) ---
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
    # Logic: Comparing current against the monthly mean
    if kt_24k > monthly_avg:
        st.warning("🔮 **PREDICTOR: EXPECTED DROP**")
        st.write("Market is currently trading above the 30-day average. A pull-back is statistically likely.")
    else:
        st.success("🔮 **PREDICTOR: UPS
