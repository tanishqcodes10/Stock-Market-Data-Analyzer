# src/analysis.py
import pandas as pd
import numpy as np


def calculate_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Daily Return = pct change of close × 100"""
    df = df.copy()
    df["daily_return"] = df["close"].pct_change() * 100
    return df


def calculate_moving_averages(df: pd.DataFrame, windows: list = None) -> pd.DataFrame:
    """Add SMA columns for each window size."""
    if windows is None:
        windows = [20, 50]
    df = df.copy()
    for w in windows:
        df[f"SMA_{w}"] = df["close"].rolling(window=w).mean()
    return df


def calculate_volatility(df: pd.DataFrame, trading_days: int = 252) -> float:
    """Annualised volatility = std(daily_return) × √252"""
    daily_std = df["daily_return"].dropna().std()
    return (daily_std * np.sqrt(trading_days)) / 100


def get_high_low_summary(df: pd.DataFrame) -> dict:
    """Returns KPI dictionary with highs, lows, returns, win/loss days."""
    idx_high = df["close"].idxmax()
    idx_low  = df["close"].idxmin()
    return {
        "highest_close"      : df.loc[idx_high, "close"],
        "highest_close_date" : df.loc[idx_high, "date"].strftime("%Y-%m-%d"),
        "lowest_close"       : df.loc[idx_low,  "close"],
        "lowest_close_date"  : df.loc[idx_low,  "date"].strftime("%Y-%m-%d"),
        "avg_close"          : df["close"].mean(),
        "total_return_pct"   : ((df["close"].iloc[-1] - df["close"].iloc[0])
                                / df["close"].iloc[0]) * 100,
        "avg_daily_return"   : df["daily_return"].dropna().mean(),
        "positive_days"      : int((df["daily_return"] > 0).sum()),
        "negative_days"      : int((df["daily_return"] < 0).sum()),
    }