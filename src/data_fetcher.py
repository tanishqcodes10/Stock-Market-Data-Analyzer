# src/data_fetcher.py

import appdirs as ad
ad.user_cache_dir = lambda *args: "/tmp"   # Fix for Streamlit Cloud

import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    try:
        # multi_level_index=False → flat columns, no MultiIndex
        df = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=True,
            progress=False,
            multi_level_index=False
        )

        if df is None or df.empty:
            return None

        # Lowercase all column names
        df.columns = [col.lower().strip() for col in df.columns]

        # Reset index so Date becomes a column
        df.reset_index(inplace=True)

        # Rename 'date' column reliably
        df.rename(
            columns={"index": "date", "Date": "date", "datetime": "date"},
            inplace=True
        )

        # Ensure date column is datetime
        df["date"] = pd.to_datetime(df["date"])

        # Keep only needed columns — drop extras like 'capital gains'
        keep = ["date", "open", "high", "low", "close", "volume"]
        df = df[[c for c in keep if c in df.columns]]

        # Drop rows where close is NaN
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