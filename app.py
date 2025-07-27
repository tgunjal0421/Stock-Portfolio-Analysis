import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import requests
import numpy as np

from dotenv import load_dotenv
import os

load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


st.set_page_config(page_title="Stock Portfolio Dashboard", layout="wide")

@st.cache_resource
def load_data():
    adjusted_df = joblib.load("data/adjusted_df.pkl")
    price_data = joblib.load("data/price_data.pkl")
    holdings_pivot = joblib.load("data/holdings_pivot.pkl")
    daily_value = joblib.load("data/daily_stocks_value.pkl")
    xirr_results = joblib.load("data/xirr_results.pkl")
    return adjusted_df, price_data, holdings_pivot, daily_value, xirr_results

adjusted_df, price_data, holdings_pivot, daily_value, xirr_results = load_data()

section = st.sidebar.radio("Navigate to:", [
    "Portfolio Overview",
    "XIRR Analysis",
    "Daily Portfolio Value",
    "Individual Stock Charts",
    "Upload New Data",
    "Latest News"
])

if section == "Portfolio Overview":
    st.title("\U0001F4C8 Portfolio Overview")
    st.dataframe(adjusted_df.head())

    st.subheader("Trade Volume by Symbol")
    volume = adjusted_df.groupby("Symbol")["Quantity"].sum().sort_values(ascending=False)
    st.bar_chart(volume)

elif section == "XIRR Analysis":
    st.title("\U0001F4CA XIRR by Stock")

    xirr_cleaned = {
        symbol: round(float(xirr) * 100, 2)
        for symbol, xirr in xirr_results.items()
        if isinstance(xirr, (float, int)) and not np.isnan(xirr)
    }

    xirr_df = pd.DataFrame({
        "Symbol": list(xirr_cleaned.keys()),
        "XIRR (%)": list(xirr_cleaned.values())
    })

    st.dataframe(xirr_df.sort_values("XIRR (%)", ascending=False))

    st.subheader("XIRR Comparison")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(xirr_df["Symbol"], xirr_df["XIRR (%)"], color="teal")
    ax.set_ylabel("XIRR (%)")
    ax.set_title("Annualized Return (XIRR) by Holding")
    ax.axhline(0, color='gray', linestyle='--')
    st.pyplot(fig)

    # Optional: XIRR for selected stock
    selected = st.selectbox("Select a stock to view XIRR", xirr_df["Symbol"])
    value = xirr_df.set_index("Symbol").loc[selected, "XIRR (%)"]
    st.metric(f"XIRR for {selected}", f"{value:.2f}%")

elif section == "Daily Portfolio Value":
    st.title("\U0001F4C5 Daily Portfolio Value")
    st.line_chart(daily_value)

elif section == "Individual Stock Charts":
    st.title("\U0001F4C9 Individual Stock Activity")
    stock = st.selectbox("Choose a stock", sorted(adjusted_df["Symbol"].unique()))

    if stock:
        subset = adjusted_df[adjusted_df["Symbol"] == stock]
        monthly_trades = subset.resample("ME", on="Date/Time")["Quantity"].sum()
        monthly_proceeds = subset.resample("ME", on="Date/Time")["Proceeds"].sum()

        st.subheader("Quantity Traded")
        st.bar_chart(monthly_trades)

        st.subheader("Proceeds")
        st.bar_chart(monthly_proceeds)

elif section == "Upload New Data":
    st.title("\U0001F4C2 Upload CSV Files")
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            df = pd.read_csv(file)
            st.success(f"Uploaded: {file.name} - {df.shape[0]} rows")
            st.dataframe(df.head())

elif section == "Latest News":
    st.title("\U0001F4F0 Latest Stock Market News")

    def fetch_stock_news():
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "stocks OR investing OR equities",
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": NEWSAPI_KEY
        }
        response = requests.get(url, params=params)
        data = response.json()
        return data.get("articles", [])[:5]

    try:
        articles = fetch_stock_news()
        for article in articles:
            st.subheader(article['title'])
            st.write(article['description'])
            st.markdown(f"[Read more]({article['url']})")
            st.markdown("---")
    except:
        st.warning("Could not fetch news. Check your API key or internet connection.")
