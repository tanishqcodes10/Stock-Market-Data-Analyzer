# src/data_fetcher.py
import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame | None:
    """Download OHLCV data from Yahoo Finance."""
    try:
        df = yf.download(ticker, start=start, end=end, auto_adjust=True, progress=False)
        if df.empty:
            return None
        df.reset_index(inplace=True)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]
        df.rename(columns={"Date": "date", "Open": "open", "High": "high",
                            "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)
        return df
    except Exception as e:
        print(f"      yfinance error: {e}")
        return None


def load_csv_fallback(path: str) -> pd.DataFrame | None:
    """Load stock data from a local CSV file."""
    try:
        df = pd.read_csv(path, parse_dates=["Date"])
        df.columns = [c.lower() for c in df.columns]
        df.rename(columns={"adj close": "close"}, inplace=True)
        df.sort_values("date", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print(f"      CSV error: {e}")
        return None