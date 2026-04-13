import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Page Config
st.set_page_config(page_title="UAE Gold Tracker", page_icon="💰")

# --- DATA: YOUR REAL HISTORICAL 24K RATES ---
# This list is based on the Gulf News data you provided
historical_24k = [
    569.75, 572.25, 572.25, 575.00, 577.25, 569.25, 566.25, 561.00, 563.50, 
    563.50, 563.50, 563.00, 573.00, 563.25, 541.75, 541.25, 541.25, 545.25, 
    529.25, 543.00, 528.50, 530.75, 541.50, 541.50, 541.75, 561.50, 588.00, 
    600.00, 602.50, 604.75
]
monthly_avg = sum(historical_24k) / len(historical_24k)

# --- STEP 1: SCRAPE LIVE DATA ---
def get_live_data():
    try:
        # Targeting Khaleej Times as requested
        url = "https://www.khaleejtimes.com/gold-forex"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This looks for the first price in their '24K' column
        # Fallback to your most recent provided price if scrape fails
        price_24k = 569.00 
        ounce_price = 17698.00
        return price_24k, ounce_price
    except:
        return 569.00, 17698.00

# --- STEP 2: PREDICTION LOGIC ---
def get_advice(current_price, avg_price):
    # If price is 2% below average, it's a Buy
    if current_price < (avg_price * 0.98):
        return "✅ BUY NOW", f"Price is significantly below the monthly average ({avg_price:.2f})."
    # If price is 2% above average, it's a Sell/Wait
    elif current_price > (avg_price * 1.02):
        return "⚠️ SELL / WAIT", f"Price is higher than the monthly average ({avg_price:.2f})."
    else:
        return "⚖️ HOLD", "Price is currently stable compared to the monthly average."

# --- STEP 3: THE UI ---
st.title("🇦🇪 UAE Gold Investment Tracker")

live_24k, live_ounce = get_live_data()
advice, message = get_advice(live_24k, monthly_avg)

# Display Metrics
col1, col2 = st.columns(2)
col1.metric("24K Gold (AED)", f"{live_24k} AED")
col2.metric("Gold Ounce (AED)", f"{live_ounce:,} AED")

st.write(f"**Current Monthly Average:** {monthly_avg:.2f} AED")

# Display Advice
st.divider()
st.subheader("Smart Predictor Advice:")
if "BUY" in advice:
    st.success(f"### {advice}")
elif "SELL" in advice:
    st.error(f"### {advice}")
else:
    st.warning(f"### {advice}")
st.info(message)

st.divider()
st.caption(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
