# 📊 Stock Portfolio Analysis Dashboard

A Streamlit-based interactive dashboard to analyze multi-year stock trading activity, compute returns (XIRR), and visualize performance across different time periods and symbols.

## 🔧 Features
- Handles multiple CSV trade files (2023–2025)
- Adjusts for stock splits
- Converts currency (USD to INR etc.)
- Calculates XIRR for each holding
- Interactive charts for portfolio value and trades
- Built with Streamlit, Matplotlib, Pandas

## 🛠 Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/STOCK_TRADING_2025.git
cd STOCK_TRADING_2025
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

