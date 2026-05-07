# streamlit_app.py — Run: streamlit run streamlit_app.py
# Disclaimer: Educational purposes only. Not financial advice.

import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns

from src.data_fetcher import fetch_stock_data
from src.data_cleaner import clean_data
from src.analysis import (calculate_daily_returns, calculate_moving_averages,
                           calculate_volatility, get_high_low_summary)

st.set_page_config(page_title="Stock Market Analyzer", page_icon="📈", layout="wide")
st.title("📈 Stock Market Data Analyzer")
st.caption("Educational tool — NOT financial advice.")

with st.sidebar:
    st.header("⚙️ Settings")
    ticker     = st.text_input("Ticker Symbol", value="AAPL").upper()
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
    end_date   = st.date_input("End Date",   value=pd.to_datetime("2024-01-01"))
    sma_windows = st.multiselect("Moving Average Windows", [10, 20, 50, 100, 200], default=[20, 50])
    run_btn = st.button("🚀 Analyse", use_container_width=True)

if run_btn:
    with st.spinner(f"Fetching data for {ticker}..."):
        df = fetch_stock_data(ticker, str(start_date), str(end_date))
        if df is None or df.empty:
            st.error("Could not fetch data. Try a different ticker or upload a CSV.")
        else:
            df = clean_data(df)
            df = calculate_daily_returns(df)
            df = calculate_moving_averages(df, windows=sma_windows)
            vol = calculate_volatility(df)
            hl  = get_high_low_summary(df)

            # KPI row
            k1, k2, k3, k4, k5 = st.columns(5)
            k1.metric("Current Price",   f"${df['close'].iloc[-1]:.2f}")
            k2.metric("Period Return",   f"{hl['total_return_pct']:.2f}%")
            k3.metric("52-Wk High",      f"${hl['highest_close']:.2f}")
            k4.metric("52-Wk Low",       f"${hl['lowest_close']:.2f}")
            k5.metric("Ann. Volatility", f"{vol:.2%}")

            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Price & Moving Averages")
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.plot(df["date"], df["close"], color="#0066CC", linewidth=1.2,
                        alpha=0.7, label="Close")
                colors_ma = ["#FF6600", "#009944", "#AA0099", "#CC8800"]
                for i, w in enumerate(sma_windows):
                    col = f"SMA_{w}"
                    if col in df.columns:
                        ax.plot(df["date"], df[col], linewidth=1.8,
                                color=colors_ma[i % len(colors_ma)], label=f"SMA {w}")
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
                plt.xticks(rotation=30, fontsize=7)
                ax.legend(fontsize=8); ax.set_ylabel("Price (USD)")
                fig.tight_layout(); st.pyplot(fig)

            with c2:
                st.subheader("Daily Returns (%)")
                fig2, ax2 = plt.subplots(figsize=(8, 4))
                clrs = df["daily_return"].apply(lambda x: "#00AA55" if x >= 0 else "#CC2200")
                ax2.bar(df["date"], df["daily_return"], color=clrs, width=1.0, alpha=0.85)
                ax2.axhline(0, color="black", linewidth=0.7)
                ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
                plt.xticks(rotation=30, fontsize=7)
                ax2.set_ylabel("Return (%)")
                fig2.tight_layout(); st.pyplot(fig2)

            st.subheader("Return Distribution")
            fig3, ax3 = plt.subplots(figsize=(10, 3))
            sns.histplot(df["daily_return"].dropna(), bins=50, kde=True,
                         color="#3366CC", edgecolor="white", linewidth=0.3, ax=ax3)
            ax3.axvline(df["daily_return"].mean(), color="red", linestyle="--",
                        linewidth=1.5, label=f"Mean: {df['daily_return'].mean():.2f}%")
            ax3.legend(); ax3.set_xlabel("Daily Return (%)")
            fig3.tight_layout(); st.pyplot(fig3)

            with st.expander("📋 View Raw Data"):
                st.dataframe(df.tail(50))

            st.success("✅ Analysis complete! — Educational use only. Not financial advice.")