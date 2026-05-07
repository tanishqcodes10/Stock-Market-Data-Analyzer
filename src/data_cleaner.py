# src/data_cleaner.py
import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Drop NaN closes, forward-fill gaps, sort, dedup, fix dtypes."""
    required_cols = {"date", "open", "high", "low", "close", "volume"}
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing expected column: {col}")

    df = df.dropna(subset=["close"])
    df = df.ffill()
    df = df.sort_values("date")
    df = df.drop_duplicates(subset=["date"])
    df.reset_index(drop=True, inplace=True)

    df["date"]   = pd.to_datetime(df["date"])
    df["close"]  = df["close"].astype(float)
    df["open"]   = df["open"].astype(float)
    df["high"]   = df["high"].astype(float)
    df["low"]    = df["low"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df