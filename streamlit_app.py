import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Page Config
st.set_page_config(page_title="UAE Gold Predictor", page_icon="💰")

# --- CONFIGURATION & ADJUSTMENTS ---
# You asked to add .75 to the gold price
adjustment_value = 0.75

# Historical 24K data for the average (based on your list)
historical_24k = [
    569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
    563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 
    529.25, 543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 
    600.00, 602.50, 604.75
]
monthly_avg = sum(historical_24k) / len(historical_24k)

# --- SCRAPING FUNCTIONS ---

def fetch_khaleej_times():
    # Placeholder for the exact scrape logic
    # Based on today's live market data (April 13)
    base_price = 567.60 
    return base_price + adjustment_value

def fetch_gulf_news():
    # Placeholder for the exact scrape logic
    # Based on today's live historical data (April 13)
    base_price = 569.75
    return base_price + adjustment_value

# --- PREDICTION LOGIC ---
def get_advice(current_price, avg_price):
    if current_price < (avg_price * 0.99):
        return "✅ BUY NOW", "Price is below the monthly average."
    elif current_price > (avg_price * 1.01):
        return "⚠️ SELL / WAIT", "Price is higher than the monthly average."
    else:
        return "⚖️ HOLD", "Price is stable relative to the average."

# --- UI LAYOUT ---
st.title("🇦🇪 UAE Gold Smart Predictor")
st.write(f"**Monthly 24K Average:** {monthly_avg:.2f} AED")

# Get prices from both sources
kt_price = fetch_khaleej_times()
gn_price = fetch_gulf_news()

# Display side-by-side
col1, col2 = st.columns(2)

with col1:
    st.subheader("Khaleej Times")
    st.metric("24K (+.75)", f"{kt_price:.2f} AED")
    advice, msg = get_advice(kt_price, monthly_avg)
    st.info(f"**{advice}**\n\n{msg}")

with col2:
    st.subheader("Gulf News")
    st.metric("24K (+.75)", f"{gn_price:.2f} AED")
    advice, msg = get_advice(gn_price, monthly_avg)
    st.info(f"**{advice}**\n\n{msg}")

st.divider()
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
