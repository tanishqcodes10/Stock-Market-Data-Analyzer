# 📈 Stock Market Data Analyzer

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Disclaimer](https://img.shields.io/badge/Disclaimer-Educational%20Only-red)

> **⚠️ Disclaimer:** This project is built for **educational purposes only**. It does **NOT** constitute financial advice, investment recommendations, or trading signals. Always consult a registered financial advisor before making any investment decisions.

---

## 📌 Project Overview

**Stock Market Data Analyzer** is a Python-based data analysis project that fetches real stock market data using the `yfinance` library (Yahoo Finance API), performs financial calculations, and generates insightful charts and reports — all without any paid data subscription.

This project demonstrates practical skills in:
- **Data Collection** (API integration, CSV handling)
- **Data Cleaning** (pandas, missing value treatment)
- **Financial Analysis** (moving averages, returns, volatility)
- **Data Visualization** (matplotlib, seaborn)
- **Report Generation** (automated text + CSV reports)
- **Dashboard Development** (Streamlit)

---

## 🎯 Problem Statement

Stock market data is publicly available but scattered and raw. Investors and analysts need:
- A clean view of price trends over time
- Moving average signals to identify buy/sell zones
- Risk quantification (volatility)
- Return performance metrics
- Automated reports — without expensive Bloomberg terminals

This project solves these needs with **100% free, open-source Python tools**.

---

## 🏭 Industry Relevance

| Role | How this project applies |
|---|---|
| **Python Developer** | Modular code, API integration, file I/O |
| **Data Analyst** | EDA, trend analysis, reporting |
| **Financial Analyst** | Returns, volatility, risk metrics |
| **Business Analyst** | Insight generation, dashboards |
| **FinTech Engineer** | Real-time data pipelines, automation |

---

## ✨ Features

- ✅ Fetch live stock data via Yahoo Finance (yfinance)
- ✅ CSV fallback for offline/historical data
- ✅ Automated data cleaning pipeline
- ✅ Daily returns calculation
- ✅ Simple Moving Averages (20-day, 50-day)
- ✅ Annualised volatility (risk indicator)
- ✅ 52-week high/low detection
- ✅ 5 publication-quality charts
- ✅ Auto-generated text + CSV reports
- ✅ Optional Streamlit interactive dashboard

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11+ | Core language |
| `yfinance` | Yahoo Finance data API |
| `pandas` | Data manipulation |
| `numpy` | Numerical calculations |
| `matplotlib` | Static charts |
| `seaborn` | Statistical plots |
| `streamlit` | Interactive dashboard |
| `plotly` | (Optional) interactive charts |

---

## 📁 Folder Structure

```
Stock-Market-Data-Analyzer/
│
├── data/               ← Raw CSV files (fallback data)
├── notebooks/          ← Jupyter notebooks for EDA
├── src/                ← Core Python modules
│   ├── data_fetcher.py
│   ├── data_cleaner.py
│   ├── analysis.py
│   ├── visualizer.py
│   └── report_generator.py
├── outputs/
│   └── charts/         ← Generated chart images
├── images/             ← Screenshots for README
├── reports/            ← Generated TXT + CSV reports
├── docs/               ← Additional documentation
├── main.py             ← Entry point
├── streamlit_app.py    ← Optional dashboard
├── requirements.txt    ← Dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Stock-Market-Data-Analyzer.git
cd Stock-Market-Data-Analyzer
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Analyzer
```bash
python main.py
```

### 5. (Optional) Run Streamlit Dashboard
```bash
streamlit run streamlit_app.py
```

---

## 📊 Sample Output

```
=======================================================
  Stock Market Data Analyzer — AAPL
  Period : 2023-01-01  →  2024-01-01
=======================================================

[1/6] Fetching stock data...
      Loaded 250 rows.
[2/6] Cleaning data...
      Clean rows: 250
[3/6] Running analysis...
      Annualised Volatility : 24.35%
      52-week High          : $198.23
      52-week Low           : $124.17
[4/6] Generating charts...
      Saved: outputs/charts/AAPL_closing_price.png
      Saved: outputs/charts/AAPL_moving_averages.png
      Saved: outputs/charts/AAPL_daily_returns.png
      Saved: outputs/charts/AAPL_return_distribution.png
      Saved: outputs/charts/AAPL_volatility.png
[5/6] Generating report...
      CSV    : reports/AAPL_data_20240101_120000.csv
      Report : reports/AAPL_summary_20240101_120000.txt
[6/6] Analysis complete!
```

---

## 📸 Screenshots

<!-- Add screenshots after running the project -->
| Chart | Description |
|---|---|
| `AAPL_closing_price.png` | Daily closing price trend |
| `AAPL_moving_averages.png` | SMA 20 & SMA 50 overlaid |
| `AAPL_daily_returns.png` | Green/red daily return bars |
| `AAPL_return_distribution.png` | Histogram + KDE of returns |
| `AAPL_volatility.png` | Rolling 30-day volatility |

---

## 🎓 Learning Outcomes

After completing this project, you will understand:
1. How to consume financial APIs with Python
2. Data cleaning best practices for time-series data
3. Calculation of financial metrics (returns, volatility, SMA)
4. Chart design with matplotlib/seaborn
5. Streamlit dashboard development
6. Modular Python project structure
7. GitHub documentation and README writing

---

## 🤝 Contributing

Pull requests are welcome. For major changes, open an issue first.

---

## 📄 License

MIT License — free for personal and educational use.

---

> **⚠️ Final Disclaimer:** This project is strictly for **learning and demonstration purposes**. Past stock performance does not predict future results. This is **NOT financial advice**.
