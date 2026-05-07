# 🗓️ Day-by-Day Proof Building Plan

Follow this plan to build GitHub commit history showing consistent daily progress.

---

## Day 1 — Project Setup

**What to do:**
- Create project folder
- Set up Python virtual environment
- Install all libraries
- Create folder structure
- Create `requirements.txt`
- Create `.gitignore`

**Commit Message:**
```
feat: initial project setup — folder structure, venv, requirements
```

**Screenshots to save:**
- `images/01_folder_structure.png` — folder tree in VS Code / terminal
- `images/02_venv_activated.png`  — terminal showing `(venv)` prompt
- `images/03_pip_install.png`     — `pip install -r requirements.txt` output

---

## Day 2 — Stock Data Fetching

**What to do:**
- Write `src/data_fetcher.py`
- Test fetching AAPL data with yfinance
- Print first 5 rows in terminal
- Save raw data as CSV to `data/AAPL_raw.csv`

**Commit Message:**
```
feat: add data fetching module — yfinance integration and CSV fallback
```

**Screenshots to save:**
- `images/04_data_fetch_terminal.png` — terminal showing row count
- `images/05_dataset_preview.png`     — first 10 rows of data

---

## Day 3 — Data Cleaning & EDA

**What to do:**
- Write `src/data_cleaner.py`
- Check for nulls, duplicates, dtype issues
- Print shape before/after cleaning
- Add a Jupyter notebook in `notebooks/EDA.ipynb`

**Commit Message:**
```
feat: add data cleaning pipeline — null handling, dtype fix, dedup
```

**Screenshots to save:**
- `images/06_cleaning_output.png`     — before/after row counts
- `images/07_notebook_eda.png`        — Jupyter notebook EDA view

---

## Day 4 — Analysis (Moving Averages & Returns)

**What to do:**
- Write `src/analysis.py`
- Test daily returns calculation
- Test SMA 20 and SMA 50
- Test volatility calculation
- Print results in terminal

**Commit Message:**
```
feat: add analysis module — returns, SMA, volatility, high/low summary
```

**Screenshots to save:**
- `images/08_analysis_terminal.png` — volatility + high/low printed

---

## Day 5 — Visualization

**What to do:**
- Write `src/visualizer.py`
- Run and verify all 5 charts save correctly
- Review chart quality

**Commit Message:**
```
feat: add visualizer — 5 charts: price, MA, returns, distribution, volatility
```

**Screenshots to save:**
- `images/09_closing_price_chart.png`
- `images/10_moving_avg_chart.png`
- `images/11_daily_returns_chart.png`
- `images/12_return_dist_chart.png`
- `images/13_volatility_chart.png`

---

## Day 6 — Report Generation, Streamlit & GitHub Documentation

**What to do:**
- Write `src/report_generator.py`
- Run full `main.py` end-to-end
- Write `streamlit_app.py` and test dashboard
- Take Streamlit screenshot
- Write `README.md`
- Push all code to GitHub

**Commit Messages:**
```
feat: add report generator — TXT summary + CSV export
feat: add streamlit dashboard — interactive stock analysis UI
docs: add README, architecture diagram, interview prep
```

**Screenshots to save:**
- `images/14_report_output.png`      — report .txt file content
- `images/15_streamlit_dashboard.png`— Streamlit running in browser
- `images/16_github_repo.png`        — GitHub repository main page

---

## GitHub Tags to Add to Repository

```
stock-market, python, data-analysis, yfinance, pandas, matplotlib,
seaborn, streamlit, financial-analysis, portfolio-project, beginner-python
```
