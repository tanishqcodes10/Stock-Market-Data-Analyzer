
from src.data_fetcher import fetch_stock_data, load_csv_fallback
from src.data_cleaner import clean_data
from src.analysis import (
    calculate_daily_returns,
    calculate_moving_averages,
    calculate_volatility,
    get_high_low_summary,
)
from src.visualizer import (
    plot_closing_price,
    plot_moving_averages,
    plot_daily_returns,
    plot_return_distribution,
    plot_volatility,
)
from src.report_generator import generate_report
import os

# ─── USER CONFIGURATION ───────────────────────────────────
TICKER     = "AAPL"
START_DATE = "2023-01-01"
END_DATE   = "2024-01-01"
CSV_PATH   = "data/AAPL.csv"
# ──────────────────────────────────────────────────────────

def main():
    print(f"\n{'='*55}")
    print(f"  Stock Market Data Analyzer — {TICKER}")
    print(f"  Period : {START_DATE}  →  {END_DATE}")
    print(f"{'='*55}\n")

    print("[1/6] Fetching stock data...")
    df = fetch_stock_data(TICKER, START_DATE, END_DATE)
    if df is None or df.empty:
        print("      yfinance failed. Trying CSV fallback...")
        df = load_csv_fallback(CSV_PATH)
    if df is None or df.empty:
        print("      ERROR: No data available. Exiting.")
        return
    print(f"      Loaded {len(df)} rows.")

    print("[2/6] Cleaning data...")
    df = clean_data(df)
    print(f"      Clean rows: {len(df)}")

    print("[3/6] Running analysis...")
    df = calculate_daily_returns(df)
    df = calculate_moving_averages(df, windows=[20, 50])
    volatility_val = calculate_volatility(df)
    high_low = get_high_low_summary(df)
    print(f"      Annualised Volatility : {volatility_val:.2%}")
    print(f"      52-week High          : ${high_low['highest_close']:.2f}")
    print(f"      52-week Low           : ${high_low['lowest_close']:.2f}")

    print("[4/6] Generating charts...")
    os.makedirs("outputs/charts", exist_ok=True)
    plot_closing_price(df, TICKER)
    plot_moving_averages(df, TICKER)
    plot_daily_returns(df, TICKER)
    plot_return_distribution(df, TICKER)
    plot_volatility(df, TICKER)

    print("[5/6] Generating report...")
    os.makedirs("reports", exist_ok=True)
    generate_report(df, TICKER, START_DATE, END_DATE, volatility_val, high_low)

    print("[6/6] Analysis complete!\n")
    print(f"{'='*55}")
    print("  DISCLAIMER: Educational purposes only.")
    print("  This is NOT financial advice.")
    print(f"{'='*55}\n")

if __name__ == "__main__":
    main()