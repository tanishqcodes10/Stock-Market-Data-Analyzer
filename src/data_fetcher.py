# src/data_fetcher.py

import appdirs as ad
from pathlib import Path

# Fix Streamlit Cloud cache dir
CACHE_DIR = ".cache"
ad.user_cache_dir = lambda *args: CACHE_DIR
Path(CACHE_DIR).mkdir(exist_ok=True)

import yfinance as yf
import pandas as pd
from curl_cffi import requests as curl_requests


def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    try:
        # Use curl_cffi session to impersonate Chrome — bypasses Yahoo rate limit
        session = curl_requests.Session(impersonate="chrome")

        tk = yf.Ticker(ticker, session=session)
        df = tk.history(start=start, end=end, auto_adjust=True)

        if df is None or df.empty:
            return None

        # Flatten and lowercase columns
        df.columns = [col.lower().strip() for col in df.columns]

        # Reset index — Date becomes a column
        df.reset_index(inplace=True)
        df.rename(columns={"date": "date", "Date": "date"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)

        # Keep only OHLCV
        keep = ["date", "open", "high", "low", "close", "volume"]
        df = df[[c for c in keep if c in df.columns]]
        df.dropna(subset=["close"], inplace=True)

        return df

    except Exception as e:
        return None


def load_csv_fallback(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        df.columns = [c.lower().strip() for c in df.columns]
        if "adj close" in df.columns:
            df.rename(columns={"adj close": "close"}, inplace=True)
        if "date" not in df.columns:
            df.rename(columns={df.columns[0]: "date"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"])
        df.dropna(subset=["close"], inplace=True)
        return df
    except Exception:
        return None