# streamlit_app.py
# Run: streamlit run streamlit_app.py
# Disclaimer: For educational purposes only. Not financial advice.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

from src.data_fetcher import fetch_stock_data
from src.data_cleaner import clean_data
from src.analysis import (
    calculate_daily_returns,
    calculate_moving_averages,
    calculate_volatility,
    get_high_low_summary,
)

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0a0e1a; color: #e2e8f0; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #161b2e 100%);
    border-right: 1px solid #1e2d4a;
}
.kpi-card {
    background: linear-gradient(135deg, #111827 0%, #1e2d4a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 20px 18px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
    margin-bottom: 4px;
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    border-radius: 14px 14px 0 0;
}
.kpi-label {
    font-size: 0.72rem; color: #64748b; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;
}
.kpi-value {
    font-size: 1.6rem; font-weight: 800; color: #f1f5f9;
    letter-spacing: -0.02em; line-height: 1.1;
}
.kpi-delta-pos { font-size: 0.78rem; color: #22c55e; font-weight: 600; margin-top: 6px; }
.kpi-delta-neg { font-size: 0.78rem; color: #ef4444; font-weight: 600; margin-top: 6px; }
.kpi-delta-neu { font-size: 0.78rem; color: #94a3b8; font-weight: 600; margin-top: 6px; }
.kpi-icon { font-size: 1.3rem; margin-bottom: 6px; }
.section-header {
    font-size: 1.05rem; font-weight: 700; color: #60a5fa;
    border-left: 3px solid #3b82f6; padding-left: 10px;
    margin: 16px 0 10px 0;
}
.ticker-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0f172a 100%);
    border: 1px solid #1e3a5f; border-radius: 14px;
    padding: 22px 28px; margin-bottom: 20px;
    display: flex; align-items: center; justify-content: space-between;
}
.ticker-name { font-size: 2rem; font-weight: 900; color: #f1f5f9; }
.ticker-subtitle { font-size: 0.78rem; color: #64748b; margin-top: 4px; }
.ticker-badge {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed);
    color: white; border-radius: 20px; padding: 6px 16px;
    font-size: 0.75rem; font-weight: 700;
}
.insight-card {
    background: linear-gradient(135deg, #0f1a2e 0%, #162032 100%);
    border: 1px solid #1e3a5f; border-radius: 12px;
    padding: 14px 16px; margin: 7px 0;
}
.insight-title {
    font-size: 0.68rem; color: #64748b; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
}
.insight-body { font-size: 0.88rem; color: #cbd5e1; margin-top: 4px; line-height: 1.5; }
.stDownloadButton button {
    background: linear-gradient(135deg, #1d4ed8, #7c3aed) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
    width: 100%; box-shadow: 0 4px 12px rgba(59,130,246,0.3) !important;
}
hr { border-color: #1e2d4a !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #1e3a5f; border-radius: 4px; }
.footer-bar {
    text-align: center; padding: 14px; margin-top: 30px;
    border-top: 1px solid #1e2d4a; font-size: 0.72rem; color: #334155;
}
</style>
""", unsafe_allow_html=True)


# ── CHART LAYOUT HELPER ────────────────────────────────────────────────────────
def dlayout(**kwargs):
    cfg = dict(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font=dict(color="#94a3b8", family="Inter, sans-serif", size=12),
        margin=dict(l=12, r=12, t=40, b=12),
        hovermode="x unified",
    )
    cfg.update(kwargs)
    return cfg


# ── CACHED DATA FETCH ──────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data(ticker, start, end, sma_tuple):
    df = fetch_stock_data(ticker, start, end)
    if df is None or df.empty:
        return None, None, None
    df  = clean_data(df)
    df  = calculate_daily_returns(df)
    df  = calculate_moving_averages(df, windows=list(sma_tuple))
    vol = calculate_volatility(df)
    hl  = get_high_low_summary(df)
    return df, vol, hl


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 Stock Analyzer")
    st.markdown("---")
    st.markdown("**Ticker Symbol**")
    POPULAR_TICKERS = {
        "🍎 Apple Inc.          (AAPL)"   : "AAPL",
        "⚡ Tesla Inc.          (TSLA)"   : "TSLA",
        "🪟 Microsoft Corp.     (MSFT)"   : "MSFT",
        "🔍 Alphabet / Google   (GOOGL)"  : "GOOGL",
        "📦 Amazon              (AMZN)"   : "AMZN",
        "🤖 NVIDIA Corp.        (NVDA)"   : "NVDA",
        "📘 Meta Platforms      (META)"   : "META",
        "🏦 Reliance Industries (RELIANCE.NS)": "RELIANCE.NS",
        "💻 Infosys Ltd.        (INFY.NS)": "INFY.NS",
        "📊 NIFTY 50 Index      (^NSEI)"  : "^NSEI",
        "✏️ Custom — type below": "__CUSTOM__",
    }

    selected_label = st.selectbox(
        "", list(POPULAR_TICKERS.keys()), index=0,
        label_visibility="collapsed"
    )

    if POPULAR_TICKERS[selected_label] == "__CUSTOM__":
        ticker = st.text_input(
            "Enter Ticker", value="BTC-USD",
            placeholder="e.g. BTC-USD, TCS.NS, ^DJI",
            label_visibility="collapsed"
        ).upper().strip()
    else:
        ticker = POPULAR_TICKERS[selected_label]
        st.markdown(
            "<div style='font-size:0.78rem; color:#60a5fa; "
            "padding: 4px 0 0 2px;'>Selected: <b>"
            + ticker + "</b></div>",
            unsafe_allow_html=True
        )

    st.markdown("**Analysis Period**")
    sc1, sc2 = st.columns(2)
    with sc1:
        start_date = st.date_input("From", value=pd.to_datetime("2023-01-01"),
                                   label_visibility="collapsed")
    with sc2:
        end_date = st.date_input("To", value=pd.to_datetime("2024-01-01"),
                                 label_visibility="collapsed")

    st.markdown("**Moving Averages**")
    sma_windows = st.multiselect("", [10, 20, 50, 100, 200], default=[20, 50])

    st.markdown("---")
    st.markdown("**Offline CSV Fallback**")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"],
                                     label_visibility="collapsed")
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.7rem;color:#334155;line-height:1.8;'>"
        "Warning: Educational tool only. "
        "Does NOT constitute financial advice.</div>",
        unsafe_allow_html=True
    )


# ── DATA LOADING ───────────────────────────────────────────────────────────────
df = vol = hl = None

if uploaded_file:
    with st.spinner("Processing uploaded CSV..."):
        try:
            raw = pd.read_csv(uploaded_file)
            raw.columns = [c.lower().strip() for c in raw.columns]
            if "adj close" in raw.columns:
                raw.rename(columns={"adj close": "close"}, inplace=True)
            if "date" not in raw.columns:
                raw.rename(columns={raw.columns[0]: "date"}, inplace=True)
            raw["date"] = pd.to_datetime(raw["date"])
            df  = clean_data(raw)
            df  = calculate_daily_returns(df)
            df  = calculate_moving_averages(df, windows=sma_windows)
            vol = calculate_volatility(df)
            hl  = get_high_low_summary(df)
        except Exception as e:
            st.error("CSV error: " + str(e))
else:
    with st.spinner("Fetching " + ticker + " from Yahoo Finance..."):
        df, vol, hl = load_data(
            ticker, str(start_date), str(end_date), tuple(sma_windows)
        )

if df is None or df.empty:
    st.error("Could not load data. Check ticker / dates, or upload a CSV.")
    st.stop()


# ── PRE-COMPUTE METRICS ────────────────────────────────────────────────────────
current_price   = float(df["close"].iloc[-1])
prev_price      = float(df["close"].iloc[-2])
price_delta     = current_price - prev_price
price_delta_pct = (price_delta / prev_price) * 100
total_return    = hl["total_return_pct"]
risk_emoji      = "🔴" if vol > 0.30 else ("🟡" if vol > 0.15 else "🟢")
risk_label      = "HIGH RISK" if vol > 0.30 else ("MEDIUM RISK" if vol > 0.15 else "LOW RISK")
avg_volume      = float(df["volume"].mean())
pos_pct         = hl["positive_days"] / (hl["positive_days"] + hl["negative_days"]) * 100
sma_colors      = ["#f97316", "#22c55e", "#a855f7", "#eab308", "#06b6d4"]

df["BB_mid"]     = df["close"].rolling(20).mean()
df["BB_upper"]   = df["BB_mid"] + 2 * df["close"].rolling(20).std()
df["BB_lower"]   = df["BB_mid"] - 2 * df["close"].rolling(20).std()
df["cum_return"] = (1 + df["daily_return"] / 100).cumprod() * 100 - 100


# ── TICKER BANNER ──────────────────────────────────────────────────────────────
trend_emoji = "📈" if total_return > 0 else "📉"
period_str  = start_date.strftime("%b %d, %Y") + "  to  " + end_date.strftime("%b %d, %Y")
st.markdown(
    '<div class="ticker-banner">'
    '<div>'
    '<div class="ticker-name">' + trend_emoji + '&nbsp; ' + ticker + '</div>'
    '<div class="ticker-subtitle">' + period_str + ' &nbsp;·&nbsp; '
    + str(len(df)) + ' trading days &nbsp;·&nbsp; </div>'
    '</div>'
    '<div class="ticker-badge">&#9679; LIVE ANALYSIS</div>'
    '</div>',
    unsafe_allow_html=True
)


# ── KPI CARDS ──────────────────────────────────────────────────────────────────
def kpi(icon, label, value, delta, dc="kpi-delta-neu"):
    return (
        '<div class="kpi-card">'
        '<div class="kpi-icon">' + icon + '</div>'
        '<div class="kpi-label">' + label + '</div>'
        '<div class="kpi-value">' + value + '</div>'
        '<div class="' + dc + '">' + delta + '</div>'
        '</div>'
    )

k1, k2, k3, k4, k5, k6 = st.columns(6)
sp   = "+" if price_delta >= 0 else ""
sr   = "+" if total_return > 0 else ""
dc_p = "kpi-delta-pos" if price_delta >= 0 else "kpi-delta-neg"
dc_r = "kpi-delta-pos" if total_return > 0 else "kpi-delta-neg"
dc_v = "kpi-delta-neg" if vol > 0.30 else ("kpi-delta-neu" if vol > 0.15 else "kpi-delta-pos")
dc_w = "kpi-delta-pos" if pos_pct >= 50 else "kpi-delta-neg"

with k1:
    st.markdown(kpi("💵", "Current Price",
        "$" + "{:.2f}".format(current_price),
        sp + "{:.2f}".format(price_delta) + " (" + sp + "{:.2f}%".format(price_delta_pct) + ")",
        dc_p), unsafe_allow_html=True)
with k2:
    st.markdown(kpi("📊", "Period Return",
        sr + "{:.2f}%".format(total_return),
        str(hl["positive_days"]) + "D up / " + str(hl["negative_days"]) + "D down",
        dc_r), unsafe_allow_html=True)
with k3:
    st.markdown(kpi("⬆️", "52-Wk High",
        "$" + "{:.2f}".format(hl["highest_close"]),
        hl["highest_close_date"], "kpi-delta-pos"), unsafe_allow_html=True)
with k4:
    st.markdown(kpi("⬇️", "52-Wk Low",
        "$" + "{:.2f}".format(hl["lowest_close"]),
        hl["lowest_close_date"], "kpi-delta-neg"), unsafe_allow_html=True)
with k5:
    st.markdown(kpi("⚡", "Ann. Volatility",
        "{:.2%}".format(vol),
        risk_emoji + " " + risk_label, dc_v), unsafe_allow_html=True)
with k6:
    st.markdown(kpi("🎯", "Win Rate",
        "{:.1f}%".format(pos_pct),
        "Avg " + "{:.3f}%".format(hl["avg_daily_return"]) + "/day",
        dc_w), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── TABS ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "🕯️  Price Action",
    "📉  Risk & Returns",
    "📊  Performance",
    "📁  Data & Export",
])


# ════════════════════════════════════════════════════════════════════════
# TAB 1 — Candlestick + Bollinger Bands + Volume
# ════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Candlestick · Bollinger Bands · Volume</div>',
                unsafe_allow_html=True)

    fig1 = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.72, 0.28]
    )

    fig1.add_trace(go.Scatter(
        x=pd.concat([df["date"], df["date"][::-1]]),
        y=pd.concat([df["BB_upper"], df["BB_lower"][::-1]]),
        fill="toself", fillcolor="rgba(99,102,241,0.07)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Bollinger Band", showlegend=True
    ), row=1, col=1)

    fig1.add_trace(go.Scatter(
        x=df["date"], y=df["BB_upper"], name="BB Upper",
        line=dict(color="#6366f1", width=1, dash="dot"), opacity=0.6
    ), row=1, col=1)
    fig1.add_trace(go.Scatter(
        x=df["date"], y=df["BB_lower"], name="BB Lower",
        line=dict(color="#6366f1", width=1, dash="dot"), opacity=0.6
    ), row=1, col=1)

    fig1.add_trace(go.Candlestick(
        x=df["date"],
        open=df["open"], high=df["high"],
        low=df["low"],   close=df["close"],
        name="OHLC",
        increasing_line_color="#22c55e", increasing_fillcolor="#22c55e",
        decreasing_line_color="#ef4444", decreasing_fillcolor="#ef4444",
        line_width=1
    ), row=1, col=1)

    for i, w in enumerate(sma_windows):
        col_name = "SMA_" + str(w)
        if col_name in df.columns:
            fig1.add_trace(go.Scatter(
                x=df["date"], y=df[col_name],
                mode="lines", name="SMA " + str(w),
                line=dict(color=sma_colors[i % len(sma_colors)], width=1.8)
            ), row=1, col=1)

    vol_clr = np.where(df["close"] >= df["open"], "#22c55e", "#ef4444")
    fig1.add_trace(go.Bar(
        x=df["date"], y=df["volume"],
        name="Volume", marker_color=vol_clr, marker_opacity=0.65
    ), row=2, col=1)
    fig1.add_trace(go.Scatter(
        x=df["date"], y=df["volume"].rolling(20).mean(),
        name="Vol MA20", line=dict(color="#f97316", width=1.4)
    ), row=2, col=1)

    fig1.update_layout(**dlayout(
        height=660,
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", y=1.02, x=0,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=11))
    ))
    fig1.update_yaxes(title_text="Price (USD)", row=1, col=1,
                      gridcolor="#1a2744", tickfont=dict(color="#64748b"))
    fig1.update_yaxes(title_text="Volume", row=2, col=1,
                      gridcolor="#1a2744", tickfont=dict(color="#64748b"))
    fig1.update_xaxes(gridcolor="#1a2744", tickfont=dict(color="#64748b"))
    st.plotly_chart(fig1, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 2 — Daily Returns + Distribution + Volatility
# ════════════════════════════════════════════════════════════════════════
with tab2:
    r1, r2 = st.columns([3, 2])

    with r1:
        st.markdown('<div class="section-header">Daily Returns (%)</div>',
                    unsafe_allow_html=True)
        fig2a = go.Figure()
        fig2a.add_trace(go.Bar(
            x=df["date"], y=df["daily_return"],
            marker_color=np.where(df["daily_return"] >= 0, "#22c55e", "#ef4444"),
            marker_opacity=0.85, name="Daily Return"
        ))
        avg_ret = float(df["daily_return"].mean())
        fig2a.add_hline(y=avg_ret, line_dash="dash", line_color="#60a5fa",
                        line_width=1.2,
                        annotation_text="Avg " + "{:.2f}%".format(avg_ret),
                        annotation_font_color="#60a5fa")
        fig2a.update_layout(**dlayout(height=340, showlegend=False))
        fig2a.update_yaxes(title_text="Return (%)", gridcolor="#1a2744",
                           tickfont=dict(color="#64748b"))
        fig2a.update_xaxes(gridcolor="#1a2744", tickfont=dict(color="#64748b"))
        st.plotly_chart(fig2a, use_container_width=True)

    with r2:
        st.markdown('<div class="section-header">Return Distribution</div>',
                    unsafe_allow_html=True)
        returns = df["daily_return"].dropna()
        fig2b = go.Figure()
        fig2b.add_trace(go.Histogram(
            x=returns, nbinsx=50,
            marker_color="#3b82f6", opacity=0.78, name="Frequency"
        ))
        fig2b.add_vline(x=float(returns.mean()), line_dash="dash",
                        line_color="#22c55e",
                        annotation_text="Mean", annotation_font_color="#22c55e")
        fig2b.add_vline(x=float(returns.mean() - returns.std()),
                        line_dash="dot", line_color="#f97316",
                        annotation_text="-1sd", annotation_font_color="#f97316")
        fig2b.add_vline(x=float(returns.mean() + returns.std()),
                        line_dash="dot", line_color="#f97316",
                        annotation_text="+1sd", annotation_font_color="#f97316")
        fig2b.update_layout(**dlayout(height=340, showlegend=False))
        fig2b.update_xaxes(title_text="Return (%)", gridcolor="#1a2744",
                            tickfont=dict(color="#64748b"))
        fig2b.update_yaxes(title_text="Frequency", gridcolor="#1a2744",
                            tickfont=dict(color="#64748b"))
        st.plotly_chart(fig2b, use_container_width=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Rolling 30-Day Volatility — Risk Zones</div>',
                unsafe_allow_html=True)

    rolling_vol = df["daily_return"].rolling(30).std() * np.sqrt(252) / 100
    max_vol     = float(max(rolling_vol.max() * 1.15, 0.4))

    fig2c = go.Figure()
    fig2c.add_hrect(y0=0.30, y1=max_vol,
                    fillcolor="rgba(239,68,68,0.06)", line_width=0)
    fig2c.add_hrect(y0=0.15, y1=0.30,
                    fillcolor="rgba(234,179,8,0.06)", line_width=0)
    fig2c.add_hrect(y0=0.0,  y1=0.15,
                    fillcolor="rgba(34,197,94,0.05)", line_width=0)
    fig2c.add_trace(go.Scatter(
        x=df["date"], y=rolling_vol, name="Volatility",
        line=dict(color="#a855f7", width=2.2),
        fill="tozeroy", fillcolor="rgba(168,85,247,0.08)"
    ))
    fig2c.add_hline(y=0.30, line_dash="dot", line_color="#ef4444",
                    annotation_text="30% High Risk",
                    annotation_font_color="#ef4444")
    fig2c.add_hline(y=0.15, line_dash="dot", line_color="#eab308",
                    annotation_text="15% Medium Risk",
                    annotation_font_color="#eab308")
    fig2c.update_layout(**dlayout(height=300))
    fig2c.update_yaxes(title_text="Volatility", gridcolor="#1a2744",
                       tickformat=".0%", tickfont=dict(color="#64748b"))
    fig2c.update_xaxes(gridcolor="#1a2744", tickfont=dict(color="#64748b"))
    st.plotly_chart(fig2c, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 3 — Cumulative Return + Insights + Monthly Heatmap
# ════════════════════════════════════════════════════════════════════════
with tab3:
    t3c1, t3c2 = st.columns([3, 2])

    with t3c1:
        st.markdown('<div class="section-header">Cumulative Return (%)</div>',
                    unsafe_allow_html=True)
        cum_end   = float(df["cum_return"].iloc[-1])
        cum_color = "#22c55e" if cum_end >= 0 else "#ef4444"
        fill_rgb  = "34,197,94" if cum_end >= 0 else "239,68,68"

        fig3a = go.Figure()
        fig3a.add_trace(go.Scatter(
            x=df["date"], y=df["cum_return"],
            mode="lines", name="Cumulative Return",
            line=dict(color=cum_color, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(" + fill_rgb + ",0.08)"
        ))
        fig3a.add_hline(y=0, line_dash="dash",
                        line_color="#475569", line_width=1)
        fig3a.update_layout(**dlayout(height=360))
        fig3a.update_yaxes(title_text="Return (%)", gridcolor="#1a2744",
                           tickformat=".1f", tickfont=dict(color="#64748b"))
        fig3a.update_xaxes(gridcolor="#1a2744", tickfont=dict(color="#64748b"))
        st.plotly_chart(fig3a, use_container_width=True)

    with t3c2:
        st.markdown('<div class="section-header">AI Insights Panel</div>',
                    unsafe_allow_html=True)
        sma20 = float(df["SMA_20"].iloc[-1]) if "SMA_20" in df.columns else None
        sma50 = float(df["SMA_50"].iloc[-1]) if "SMA_50" in df.columns else None
        if sma20 and sma50:
            trend_sig = ("🟢 Bullish — Golden Cross zone"
                         if sma20 > sma50 else "🔴 Bearish — Death Cross zone")
        else:
            trend_sig = "Select MAs in sidebar"

        insights = [
            ("Trend Signal",
             trend_sig),
            ("Period Performance",
             ("Gained " if total_return > 0 else "Lost ") + "{:.2f}%".format(abs(total_return)) + " over period"),
            ("Risk Assessment",
             risk_emoji + " " + risk_label + " — " + "{:.2%}".format(vol) + " annualised"),
            ("Win Rate",
             "{:.1f}%".format(pos_pct) + " positive days (" + str(hl["positive_days"]) + " up, " + str(hl["negative_days"]) + " down)"),
            ("Price Range",
             "$" + "{:.2f}".format(hl["lowest_close"]) + " to $" + "{:.2f}".format(hl["highest_close"])),
            ("Avg Daily Return",
             "{:.4f}%".format(hl["avg_daily_return"]) + " per trading day"),
        ]
        for title_i, body_i in insights:
            st.markdown(
                '<div class="insight-card">'
                '<div class="insight-title">' + title_i + '</div>'
                '<div class="insight-body">' + body_i + '</div>'
                '</div>',
                unsafe_allow_html=True
            )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">Monthly Return Heatmap</div>',
                unsafe_allow_html=True)

    df_m = df.copy()
    df_m["year"]  = df_m["date"].dt.year
    df_m["month"] = df_m["date"].dt.month
    monthly = df_m.groupby(["year", "month"])["daily_return"].sum().reset_index()
    monthly.columns = ["Year", "Month", "Return"]
    mnames = ["Jan","Feb","Mar","Apr","May","Jun",
              "Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly["MN"] = monthly["Month"].apply(lambda x: mnames[x - 1])
    pivot = monthly.pivot(index="Year", columns="MN", values="Return")
    ordered = [m for m in mnames if m in pivot.columns]
    pivot = pivot[ordered]

    fig3b = go.Figure(go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=[str(y) for y in pivot.index],
        colorscale=[[0, "#ef4444"], [0.5, "#0d1117"], [1, "#22c55e"]],
        text=np.round(pivot.values, 1),
        texttemplate="%{text}%",
        textfont=dict(size=11, color="white"),
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#94a3b8"),
            tickformat=".0f",
            title=dict(text="Ret%", font=dict(color="#94a3b8"))
        )
    ))
    fig3b.update_layout(**dlayout(height=210))
    fig3b.update_xaxes(tickfont=dict(color="#94a3b8"), side="bottom")
    fig3b.update_yaxes(tickfont=dict(color="#94a3b8"))
    st.plotly_chart(fig3b, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════
# TAB 4 — Data & Export
# ════════════════════════════════════════════════════════════════════════
with tab4:
    t4c1, t4c2 = st.columns([3, 2])

    with t4c1:
        st.markdown('<div class="section-header">Processed Dataset (Last 60 Rows)</div>',
                    unsafe_allow_html=True)
        display_cols = ["date", "open", "high", "low", "close", "volume", "daily_return"]
        for col in ["SMA_" + str(w) for w in sma_windows]:
            if col in df.columns:
                display_cols.append(col)
        fmt = {
            "open": "${:.2f}", "high": "${:.2f}",
            "low": "${:.2f}",  "close": "${:.2f}",
            "volume": "{:,.0f}", "daily_return": "{:.2f}%"
        }
        for col in ["SMA_" + str(w) for w in sma_windows]:
            fmt[col] = "${:.2f}"
        st.dataframe(
            df[display_cols].tail(60).style.format(fmt),
            use_container_width=True, height=500
        )

    with t4c2:
        st.markdown('<div class="section-header">Export</div>',
                    unsafe_allow_html=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M")

        st.download_button(
            label="Download Dataset (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=ticker + "_analyzed_" + ts + ".csv",
            mime="text/csv",
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        sep = "=" * 45
        report_lines = [
            "STOCK ANALYSIS REPORT",
            sep,
            "Ticker    : " + ticker,
            "Period    : " + str(start_date) + " to " + str(end_date),
            "Generated : " + datetime.now().strftime("%Y-%m-%d %H:%M"),
            "",
            "PRICE   High $" + "{:.2f}".format(hl["highest_close"])
            + " | Low $" + "{:.2f}".format(hl["lowest_close"])
            + " | Avg $" + "{:.2f}".format(hl["avg_close"]),
            "RETURN  Total " + "{:.2f}%".format(total_return)
            + " | Daily Avg " + "{:.4f}%".format(hl["avg_daily_return"]),
            "RISK    Volatility " + "{:.2%}".format(vol) + " | " + risk_label,
            "DAYS    Win " + str(hl["positive_days"])
            + " | Loss " + str(hl["negative_days"])
            + " | Rate " + "{:.1f}%".format(pos_pct),
            sep,
            "DISCLAIMER: Educational only. NOT financial advice.",
        ]
        summary = "\n".join(report_lines)

        st.download_button(
            label="Download Summary (TXT)",
            data=summary.encode("utf-8"),
            file_name=ticker + "_summary_" + ts + ".txt",
            mime="text/plain",
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">Quick Stats</div>',
                    unsafe_allow_html=True)
        st.dataframe(
            pd.DataFrame([
                ("Trading Days",    len(df)),
                ("Avg Volume",      "{:.1f}M".format(avg_volume / 1e6)),
                ("Current Price",   "$" + "{:.2f}".format(current_price)),
                ("Total Return",    "{:.2f}%".format(total_return)),
                ("Ann. Volatility", "{:.2%}".format(vol)),
                ("Risk Level",      risk_emoji + " " + risk_label),
                ("Win Rate",        "{:.1f}%".format(pos_pct)),
                ("Avg Daily Ret",   "{:.3f}%".format(hl["avg_daily_return"])),
                ("52-Wk High",      "$" + "{:.2f}".format(hl["highest_close"])),
                ("52-Wk Low",       "$" + "{:.2f}".format(hl["lowest_close"])),
            ], columns=["Metric", "Value"]),
            use_container_width=True, hide_index=True, height=380
        )


# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer-bar">'
    'Built with Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Plotly'
    '&nbsp;|&nbsp; Data: Yahoo Finance via yfinance'
    '&nbsp;|&nbsp; <b>Educational purposes only — NOT financial advice</b>'
    '</div>',
    unsafe_allow_html=True
)