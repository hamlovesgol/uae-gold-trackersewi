import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Page Config
st.set_page_config(page_title="UAE Gold Predictor Pro", page_icon="💰", layout="wide")

# --- DATA & CONSTANTS ---
# Historical data from your provided list (30 days)
hist_prices = [
    569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
    563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 
    529.25, 543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 
    600.00, 602.50, 604.75
]
monthly_avg = sum(hist_prices) / len(hist_prices)
current_price = 569.75  # Newest price from your screenshot

# --- APP UI ---
st.title("🇦🇪 UAE Gold Investment Pro")

# 1. LIVE METRICS
m1, m2, m3 = st.columns(3)
m1.metric("Current 24K (AED)", f"{current_price}")
m2.metric("Monthly Average", f"{monthly_avg:.2f}")
m3.metric("Market Status", "Stable" if abs(current_price - monthly_avg) < 5 else "Volatile")

st.divider()

# 2. SMART INVESTMENT ADVICE & PREDICTOR
st.subheader("🤖 Smart Predictor & Targets")
col_a, col_b = st.columns(2)

with col_a:
    st.write("### 🔮 Next-Move Predictor")
    if current_price > monthly_avg:
        st.error("**Forecast: LIKELY LOWER**")
        st.write("Price is currently above the 30-day mean. Expect a correction soon.")
    else:
        st.success("**Forecast: LIKELY HIGHER**")
        st.write("Price is below or near the average. Upside potential is higher.")

with col_b:
    st.write("### 🎯 Perfect Entry/Exit Targets")
    st.write(f"**Short Term (1-4 Weeks):** Buy at **{monthly_avg*0.97:.1f}**, Sell at **{monthly_avg*1.03:.1f}**")
    st.write(f"**Mid Term (3-6 Months):** Buy at **{monthly_avg*0.95:.1f}**, Sell at **{monthly_avg*1.08:.1f}**")
    st.write(f"**Long Term (7+ Months):** Buy at **{monthly_avg*0.93:.1f}**, Sell at **{monthly_avg*1.15:.1f}**")

st.divider()

# 3. THE "TRIAL & ERROR" PROFIT GAME
st.subheader("🎮 Investment Simulator (Trial & Error)")
st.write("Test your strategy! See what happens if you buy now and the price changes.")

sim_col1, sim_col2, sim_col3 = st.columns(3)

with sim_col1:
    buy_price = st.number_input("Your Buy Price (AED)", value=current_price)
with sim_col2:
    investment = st.number_input("Amount to Invest (AED)", value=1000)
with sim_col3:
    future_price = st.slider("Test a Future Price (AED)", min_value=450.0, max_value=650.0, value=current_price + 10)

# Calculations
grams_bought = investment / buy_price
current_value = grams_bought * future_price
profit = current_value - investment
profit_percent = (profit / investment) * 100

st.write("---")
if profit > 0:
    st.balloons()
    st.success(f"**Result:** If price hits **{future_price}**, your profit is **{profit:.2f} AED** ({profit_percent:.1f}%)")
else:
    st.error(f"**Result:** If price hits **{future_price}**, your loss is **{abs(profit):.2f} AED** ({profit_percent:.1f}%)")

st.divider()

# 4. PRICE TREND
st.subheader("📊 24K Price Trend (Newest to Oldest)")
hist_dates = [f"{i} Apr" for i in range(13, 0, -1)] + [f"{i} Mar" for i in range(31, 14, -1)]
df = pd.DataFrame({'Date': hist_dates, 'Price (AED)': hist_prices})
st.line_chart(df.set_index('Date'))
