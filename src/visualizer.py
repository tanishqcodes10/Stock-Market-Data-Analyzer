# src/visualizer.py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import numpy as np
import pandas as pd

CHART_DIR = "outputs/charts"
STYLE     = "seaborn-v0_8-darkgrid"


def _save(fig, filename: str):
    path = f"{CHART_DIR}/{filename}"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"      Saved: {path}")


def plot_closing_price(df: pd.DataFrame, ticker: str):
    """Line chart of daily closing price."""
    fig, ax = plt.subplots(figsize=(12, 5))
    plt.style.use(STYLE)
    ax.plot(df["date"], df["close"], color="#0066CC", linewidth=1.5, label="Close Price")
    ax.fill_between(df["date"], df["close"], alpha=0.08, color="#0066CC")
    ax.set_title(f"{ticker} — Closing Price", fontsize=15, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Price (USD)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.legend(); fig.tight_layout()
    _save(fig, f"{ticker}_closing_price.png")


def plot_moving_averages(df: pd.DataFrame, ticker: str):
    """Closing price with SMA_20 and SMA_50 overlaid."""
    fig, ax = plt.subplots(figsize=(12, 5))
    plt.style.use(STYLE)
    ax.plot(df["date"], df["close"],  color="#888888", linewidth=1.0, alpha=0.6, label="Close")
    if "SMA_20" in df.columns:
        ax.plot(df["date"], df["SMA_20"], color="#FF6600", linewidth=1.8, label="20-Day SMA")
    if "SMA_50" in df.columns:
        ax.plot(df["date"], df["SMA_50"], color="#009944", linewidth=1.8, label="50-Day SMA")
    ax.set_title(f"{ticker} — Moving Averages", fontsize=15, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Price (USD)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.legend(); fig.tight_layout()
    _save(fig, f"{ticker}_moving_averages.png")


def plot_daily_returns(df: pd.DataFrame, ticker: str):
    """Green/red bar chart of daily returns."""
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.style.use(STYLE)
    colors = df["daily_return"].apply(lambda x: "#00AA55" if x >= 0 else "#CC2200")
    ax.bar(df["date"], df["daily_return"], color=colors, width=1.0, alpha=0.85)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"{ticker} — Daily Returns (%)", fontsize=15, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Return (%)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30); fig.tight_layout()
    _save(fig, f"{ticker}_daily_returns.png")


def plot_return_distribution(df: pd.DataFrame, ticker: str):
    """Histogram + KDE of daily return distribution."""
    returns = df["daily_return"].dropna()
    fig, ax = plt.subplots(figsize=(8, 5))
    plt.style.use(STYLE)
    sns.histplot(returns, bins=40, kde=True, color="#3366CC",
                 edgecolor="white", linewidth=0.4, ax=ax)
    ax.axvline(returns.mean(), color="red", linestyle="--", linewidth=1.5,
               label=f"Mean: {returns.mean():.2f}%")
    ax.axvline(returns.std(), color="orange", linestyle="--", linewidth=1.5,
               label=f"Std Dev: {returns.std():.2f}%")
    ax.set_title(f"{ticker} — Return Distribution", fontsize=15, fontweight="bold")
    ax.set_xlabel("Daily Return (%)"); ax.set_ylabel("Frequency")
    ax.legend(); fig.tight_layout()
    _save(fig, f"{ticker}_return_distribution.png")


def plot_volatility(df: pd.DataFrame, ticker: str, window: int = 30):
    """Rolling 30-day annualised volatility line chart."""
    rolling_vol = df["daily_return"].rolling(window).std() * np.sqrt(252) / 100
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.style.use(STYLE)
    ax.plot(df["date"], rolling_vol, color="#990066", linewidth=1.5,
            label=f"{window}-Day Rolling Volatility")
    ax.fill_between(df["date"], rolling_vol, alpha=0.1, color="#990066")
    ax.set_title(f"{ticker} — Rolling Volatility ({window}-Day)", fontsize=15, fontweight="bold")
    ax.set_xlabel("Date"); ax.set_ylabel("Volatility (Annualised)")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.xticks(rotation=30)
    ax.legend(); fig.tight_layout()
    _save(fig, f"{ticker}_volatility.png")