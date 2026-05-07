# src/report_generator.py
# Generates a plain-text and CSV summary report.
# Disclaimer: For educational purposes only. Not financial advice.

import pandas as pd
from datetime import datetime


def generate_report(df, ticker, start, end, volatility, high_low):
    """Save both a .txt summary and a .csv of the clean data."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # CSV export
    csv_path = f"reports/{ticker}_data_{timestamp}.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # Text report
    txt_path = f"reports/{ticker}_summary_{timestamp}.txt"

    lines = [
        "=" * 55,
        "  STOCK MARKET ANALYSIS REPORT",
        f"  Ticker : {ticker}",
        f"  Period : {start}  to  {end}",
        f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 55,
        "",
        "-- PRICE SUMMARY --",
        f"  Highest Close : ${high_low['highest_close']:.2f} on {high_low['highest_close_date']}",
        f"  Lowest  Close : ${high_low['lowest_close']:.2f} on {high_low['lowest_close_date']}",
        f"  Average Close : ${high_low['avg_close']:.2f}",
        "",
        "-- RETURN ANALYSIS --",
        f"  Total Period Return   : {high_low['total_return_pct']:.2f}%",
        f"  Average Daily Return  : {high_low['avg_daily_return']:.4f}%",
        f"  Positive Trading Days : {high_low['positive_days']}",
        f"  Negative Trading Days : {high_low['negative_days']}",
        "",
        "-- RISK ANALYSIS --",
        f"  Annualised Volatility : {volatility:.2%}",
        f"  Risk Level            : {'HIGH' if volatility > 0.30 else 'MEDIUM' if volatility > 0.15 else 'LOW'}",
        "",
        "-- CHARTS GENERATED --",
        f"  outputs/charts/{ticker}_closing_price.png",
        f"  outputs/charts/{ticker}_moving_averages.png",
        f"  outputs/charts/{ticker}_daily_returns.png",
        f"  outputs/charts/{ticker}_return_distribution.png",
        f"  outputs/charts/{ticker}_volatility.png",
        "",
        "=" * 55,
        "  DISCLAIMER: This report is for EDUCATIONAL PURPOSES",
        "  ONLY. It does NOT constitute financial advice.",
        "  Always consult a registered financial advisor.",
        "=" * 55,
    ]

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"      CSV    : {csv_path}")
    print(f"      Report : {txt_path}")