import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy_financial as npf

# -----------------------------
# Assume all your precomputed data is loaded here
# -----------------------------

import joblib

adjusted_df = joblib.load("data/adjusted_df.pkl")
price_data = joblib.load("data/price_data.pkl")
holdings_pivot = joblib.load("data/holdings_pivot.pkl")
daily_portfolio_value = joblib.load("data/daily_stocks_value.pkl")
xirr_results = joblib.load("data/xirr_results.pkl")


st.set_page_config(page_title="Stock Portfolio Dashboard", layout="wide")
st.title("📈 Stock Portfolio Analysis Dashboard")

# -----------------------------
# Section 1: Portfolio Summary
# -----------------------------
st.header("Portfolio Summary")
st.markdown("This dashboard visualizes trades, prices, portfolio value over time, and XIRR for each holding.")

col1, col2 = st.columns(2)
with col1:
    total_current_value = daily_portfolio_value['Total Value'].iloc[-1]
    st.metric("💰 Current Portfolio Value", f"${total_current_value:,.2f}")
with col2:
    total_holdings = holdings_pivot.iloc[-1].astype(bool).sum()
    st.metric("📦 Active Holdings", f"{total_holdings}")

# -----------------------------
# Section 2: Holdings Overview
# -----------------------------
st.subheader("📊 Holdings Snapshot")
st.dataframe(holdings_pivot.iloc[-1].to_frame(name='Quantity').sort_values(by='Quantity', ascending=False))

# -----------------------------
# Section 3: Portfolio Value Over Time
# -----------------------------
st.subheader("📉 Portfolio Value Over Time")
fig1, ax1 = plt.subplots(figsize=(12, 4))
daily_portfolio_value['Total Value'].plot(ax=ax1, color='green')
ax1.set_title("Daily Total Portfolio Value")
ax1.set_ylabel("Value in USD")
ax1.grid(True, linestyle='--', alpha=0.3)
st.pyplot(fig1)

# -----------------------------
# Section 4: XIRR by Symbol
# -----------------------------
st.subheader("📈 XIRR by Stock Holding")

# Filter valid results
valid_xirr = {
    sym: val for sym, val in xirr_results.items()
    if isinstance(val, (float, int)) and not np.isnan(val)
}

if valid_xirr:
    xirr_df = pd.DataFrame(list(valid_xirr.items()), columns=['Symbol', 'XIRR'])
    xirr_df = xirr_df.sort_values('XIRR', ascending=False)
    st.dataframe(xirr_df.style.format({'XIRR': "{:.2%}"}))

    # Plot
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    colors = ['teal' if x >= 0 else 'crimson' for x in xirr_df['XIRR']]
    ax2.bar(xirr_df['Symbol'], xirr_df['XIRR'], color=colors)
    ax2.set_title("Annualized Return (XIRR) per Holding")
    ax2.axhline(0, linestyle='--', color='gray')
    ax2.set_ylabel("XIRR (%)")
    for idx, val in enumerate(xirr_df['XIRR']):
        ax2.text(idx, val, f"{val:.1%}", ha='center', va='bottom', fontsize=8)
    st.pyplot(fig2)
else:
    st.info("No valid XIRR results to display.")

# -----------------------------
# (Optional) Section 5: Upload New File
# -----------------------------
st.subheader("📁 Upload New Trade File")
uploaded_file = st.file_uploader("Upload your trade Excel/CSV file to re-run the analysis", type=["csv", "xlsx"])
if uploaded_file:
    st.warning("You can now process this file in your backend pipeline.")

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
