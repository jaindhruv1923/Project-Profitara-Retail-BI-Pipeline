import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings("ignore")

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Profitara Golden — Retail Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS — matching HTML dashboard exactly ──────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700&family=IBM+Plex+Mono:wght@400;600&display=swap');

:root {
  --ink: #1A1F2B;
  --ink-soft: #4A5568;
  --paper: #F7F6F2;
  --card: #FFFFFF;
  --line: #D9DCE3;
  --teal: #1B3A5C;
  --teal-soft: #E4EAF1;
  --amber: #C9971F;
  --amber-soft: #FCF1D9;
  --good: #2F7D4F;
  --good-soft: #E5F2E9;
  --risk: #B23A3A;
  --risk-soft: #FBEAEA;
  --warn: #B8860B;
  --warn-soft: #FCF3DD;
}

html, body {
  font-family: 'Atkinson Hyperlegible', sans-serif;
  color: var(--ink);
}

/* Force the actual app background to light paper — these are the stable
   containers in current Streamlit versions (the old [class*="css"] trick
   stopped matching anything after Streamlit renamed its internal classes) */
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
.stApp,
.main {
  background: var(--paper) !important;
  color: var(--ink);
}
[data-testid="stHeader"] {
  background: transparent !important;
}

/* Universal safety net: force every text element to a visible dark color
   by default. Specific rules below (badges, kpi values, etc.) override
   this where a different color is intentional. This prevents any element
   from silently inheriting an invisible color from Streamlit's theme. */
[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] label,
[data-testid="stAppViewContainer"] li,
[data-testid="stMarkdownContainer"] {
  color: var(--ink);
}
[data-testid="stDataFrame"], [data-testid="stTable"] {
  background: #FFFFFF !important;
}

/* Dropdown/select popovers render outside the main container (appended to
   body), so the earlier text-color safety net never reached them. Fix
   explicitly, at every nesting layer BaseWeb uses. */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="layer"],
[data-baseweb="menu"],
ul[data-baseweb="menu"],
[role="listbox"] {
  background: #FFFFFF !important;
  background-color: #FFFFFF !important;
}
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[role="listbox"] * {
  color: var(--ink) !important;
  background-color: transparent;
}
li[role="option"],
[data-baseweb="menu-item"],
[data-testid="stSelectboxVirtualDropdown"] li {
  background-color: #FFFFFF !important;
  color: var(--ink) !important;
}
li[role="option"]:hover,
[data-baseweb="menu-item"]:hover {
  background-color: var(--teal-soft) !important;
}
[data-testid="stSelectboxVirtualDropdown"] {
  background: #FFFFFF !important;
}
[data-testid="stSelectbox"] {
  background: #FFFFFF !important;
}
[data-baseweb="select"] {
  background: #FFFFFF !important;
}
[data-baseweb="select"] > div {
  background: #FFFFFF !important;
  border-color: var(--line) !important;
}
[data-baseweb="select"] * {
  color: var(--ink) !important;
}

/* Tabs */
[data-testid="stTabs"] button {
  color: var(--ink-soft) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--teal) !important;
}

/* Metrics */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"], [data-testid="stMetricDelta"] {
  color: var(--ink) !important;
}

/* Expanders */
[data-testid="stExpander"] {
  background: #FFFFFF !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px !important;
}
[data-testid="stExpander"] * {
  color: var(--ink) !important;
}

/* Text inputs, text areas, number inputs, sliders */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
  background: #FFFFFF !important;
  color: var(--ink) !important;
}
[data-testid="stSlider"] label {
  color: var(--ink) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
  background: #FFFFFF !important;
  border: 1.5px dashed var(--line) !important;
  border-radius: 10px !important;
  padding: 0.5rem !important;
}
[data-testid="stFileUploader"] section {
  background: #FFFFFF !important;
}
[data-testid="stFileUploaderDropzone"] {
  background: #FFFFFF !important;
}
[data-testid="stFileUploader"] * {
  color: var(--ink) !important;
}
[data-testid="stFileUploader"] button {
  background: var(--teal) !important;
  color: #FFFFFF !important;
  border-radius: 6px !important;
}
[data-testid="stFileUploader"] button * {
  color: #FFFFFF !important;
}

/* Hide Streamlit chrome but KEEP the sidebar toggle arrow working in BOTH states */
#MainMenu, footer { visibility: hidden; }
header { visibility: visible; background: transparent; box-shadow: none; z-index: 999999 !important; }
header [data-testid="stToolbar"] { visibility: hidden; }
[data-testid="collapsedControl"] {
  visibility: visible !important;
  display: flex !important;
  position: fixed !important;
  top: 0.5rem !important;
  left: 0.5rem !important;
  z-index: 999999 !important;
  background: #FFFFFF !important;
  border: 2px solid #D9DCE3 !important;
  border-radius: 8px !important;
}
[data-testid="stSidebarCollapsedControl"] {
  visibility: visible !important;
  display: flex !important;
  position: fixed !important;
  top: 0.5rem !important;
  left: 0.5rem !important;
  z-index: 999999 !important;
  background: #FFFFFF !important;
  border: 2px solid #D9DCE3 !important;
  border-radius: 8px !important;
}
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] {
  background: #FFFFFF;
  border-right: 2px solid #D9DCE3;
}
section[data-testid="stSidebar"] * {
  color: #1A1F2B !important;
}
section[data-testid="stSidebar"] .stMarkdown h2 {
  color: #1B3A5C; font-size: 1.1rem; border-bottom: 2px solid #D9DCE3;
  padding-bottom: 0.5rem; margin-bottom: 0.5rem;
}

/* Top bar title */
.topbar-title {
  color: #1B3A5C; font-size: 2rem; font-weight: 700; letter-spacing: .02em;
  margin: 0; font-family: 'Atkinson Hyperlegible', sans-serif;
}
.topbar-sub { color: #4A5568; font-size: 1rem; margin-top: .2rem; }

/* Section headers */
.eyebrow {
  font-size: .85rem; text-transform: uppercase; letter-spacing: .12em;
  color: #C9971F; font-weight: 700; margin-bottom: .2rem;
}
.section-h2 {
  color: #1B3A5C; font-size: 1.7rem; font-weight: 700;
  margin-bottom: .3rem; font-family: 'Atkinson Hyperlegible', sans-serif;
}
.lede { color: #4A5568; font-size: 1.05rem; margin-bottom: 1rem; }

/* KPI Cards */
.kpi-card {
  background: #FFFFFF; border: 2px solid #D9DCE3; border-radius: 14px;
  padding: 1.25rem 1.5rem; text-align: left;
}
.kpi-val {
  font-family: 'IBM Plex Mono', monospace; font-size: 1.8rem;
  font-weight: 600; color: #1B3A5C; display: block;
}
.kpi-lab { font-size: .9rem; color: #4A5568; }
.kpi-delta { font-size: .85rem; margin-top: .3rem; }
.kpi-delta.good { color: #2F7D4F; }
.kpi-delta.risk { color: #B23A3A; }

/* Cards */
.info-card {
  background: #FFFFFF; border: 2px solid #D9DCE3; border-radius: 14px;
  padding: 1.5rem; margin-bottom: .75rem;
}
.info-card h3 { color: #1A1F2B; font-size: 1.1rem; margin-bottom: .5rem; }
.info-card p  { color: #4A5568; font-size: .95rem; }

/* Teal card */
.teal-card {
  background: #E4EAF1; border: 2px solid #1B3A5C; border-radius: 14px;
  padding: 1.5rem; margin-bottom: .75rem;
}
.teal-card h3 { color: #1B3A5C; }

/* Amber card */
.amber-card {
  background: #FCF1D9; border: 2px solid #C9971F; border-radius: 14px;
  padding: 1.25rem 1.5rem;
}

/* Good / warn / risk insight boxes */
.insight-good {
  background: #E5F2E9; border-left: 4px solid #2F7D4F;
  padding: .9rem 1rem; border-radius: 0 8px 8px 0; margin-top: .75rem;
  font-size: .95rem; color: #1A1F2B;
}
.insight-warn {
  background: #FCF3DD; border-left: 4px solid #B8860B;
  padding: .9rem 1rem; border-radius: 0 8px 8px 0; margin-top: .75rem;
  font-size: .95rem; color: #1A1F2B;
}
.insight-risk {
  background: #FBEAEA; border-left: 4px solid #B23A3A;
  padding: .9rem 1rem; border-radius: 0 8px 8px 0; margin-top: .75rem;
  font-size: .95rem; color: #1A1F2B;
}

/* Health scorecard circle */
.health-circle {
  width: 140px; height: 140px; border-radius: 50%;
  border: 8px solid #1B3A5C; background: #E4EAF1;
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; margin: auto;
}
.health-num {
  font-family: 'IBM Plex Mono', monospace; font-size: 2.4rem;
  font-weight: 700; color: #1B3A5C;
}
.health-lbl { font-size: .8rem; color: #4A5568; }

/* Badge */
.badge-good  { background: #E5F2E9; color: #2F7D4F; padding: .2rem .6rem; border-radius: 999px; font-size: .85rem; font-weight: 700; }
.badge-warn  { background: #FCF3DD; color: #B8860B; padding: .2rem .6rem; border-radius: 999px; font-size: .85rem; font-weight: 700; }
.badge-risk  { background: #FBEAEA; color: #B23A3A; padding: .2rem .6rem; border-radius: 999px; font-size: .85rem; font-weight: 700; }

/* Golden tag */
.golden-tag {
  display: inline-block; background: #C9971F; color: #fff; font-weight: 700;
  font-size: .8rem; padding: .2rem .7rem; border-radius: 999px;
  margin-bottom: .5rem; letter-spacing: .06em;
}

/* Divider */
.section-divider { border: none; border-top: 2px solid #D9DCE3; margin: 2rem 0; }

/* Table styling */
.dataframe { width: 100%; border-collapse: collapse; font-size: .9rem; }
.dataframe th { background: #F7F6F2; color: #4A5568; text-transform: uppercase;
  font-size: .78rem; letter-spacing: .08em; border-bottom: 2px solid #D9DCE3;
  padding: .5rem .75rem; }
.dataframe td { padding: .5rem .75rem; border-bottom: 1px solid #D9DCE3; }

/* Mono numbers */
.mono { font-family: 'IBM Plex Mono', monospace; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file_path=None, uploaded=None):
    if uploaded is not None:
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_csv("Profitara_India_Dataset.csv")
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=False)
    df['Month']      = df['Order Date'].dt.to_period('M').astype(str)
    df['Year']       = df['Order Date'].dt.year
    df['Quarter']    = df['Order Date'].dt.to_period('Q').astype(str)
    df['Margin %']   = (df['Profit'] / df['Sales'].replace(0, np.nan) * 100).round(2)
    return df


# ─── PLOTLY COLOUR PALETTE ───────────────────────────────────────────────────
TEAL     = "#1B3A5C"
AMBER    = "#C9971F"
GOOD     = "#2F7D4F"
RISK     = "#B23A3A"
WARN     = "#B8860B"
PAPER    = "#F7F6F2"
INK      = "#1A1F2B"
INK_SOFT = "#4A5568"
LINE     = "#D9DCE3"

CAT_COLORS = [TEAL, AMBER, GOOD, RISK, WARN, "#5E81AC", "#88C0D0", "#BF616A", "#A3BE8C", "#EBCB8B"]

CHART_LAYOUT = dict(
    paper_bgcolor=PAPER,
    plot_bgcolor=PAPER,
    font=dict(family="Atkinson Hyperlegible, sans-serif", color=INK, size=13),
    title_font=dict(color=INK, size=16, family="Atkinson Hyperlegible, sans-serif"),
    title_x=0.02,
    title_xanchor="left",
    margin=dict(l=10, r=10, t=55, b=10),
    legend=dict(bgcolor="rgba(255,255,255,0.85)", bordercolor=LINE, borderwidth=1, font=dict(color=INK, size=12)),
)


def styled_chart(fig):
    fig.update_layout(**CHART_LAYOUT)
    fig.update_annotations(font=dict(color=INK, size=13, family="Atkinson Hyperlegible, sans-serif"))
    fig.update_xaxes(
        gridcolor=LINE, zerolinecolor=LINE,
        tickfont=dict(color=INK, size=12, family="Atkinson Hyperlegible, sans-serif"),
        title_font=dict(color=INK, size=13, family="Atkinson Hyperlegible, sans-serif"),
        linecolor=LINE,
    )
    fig.update_yaxes(
        gridcolor=LINE, zerolinecolor=LINE,
        tickfont=dict(color=INK, size=12, family="Atkinson Hyperlegible, sans-serif"),
        title_font=dict(color=INK, size=13, family="Atkinson Hyperlegible, sans-serif"),
        linecolor=LINE,
    )
    return fig


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2>PROFITARA GOLDEN</h2>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:.8rem;color:#C9971F;font-weight:700;margin-bottom:.25rem'>▸ GOLDEN FEATURES</div>", unsafe_allow_html=True)
    page = st.radio("", [
        "🏠 Overview & Health",
        "📊 Core KPIs",
        "📈 Sales & Categories",
        "🛒 Products & Discounts",
        "💡 Elasticity Simulator",
        "🔗 Market Basket Analysis",
        "⚠️ Churn Early Warning",
        "📉 Cohort Retention",
        "🗺️ Geo Intelligence",
        "💸 Leakage & Abuse",
        "🤖 12 ML Modules",
        "🔮 Forecasts & Trends",
        "🧮 SQL Analytics Lab",
    ], label_visibility="collapsed")
    st.markdown("<hr style='border-color:#D9DCE3'>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("📁 Upload your own CSV", type=["csv"],
                                     help="Drop any Superstore-style CSV to re-run all modules")
    st.markdown("<div style='font-size:.8rem;color:#4A5568;margin-top:.5rem'>Built by <strong>Dhruv Jain</strong> · BML Munjal University</div>", unsafe_allow_html=True)


# ─── LOAD DATA ───────────────────────────────────────────────────────────────
if uploaded_file is None:
    st.markdown("""
    <div style="background:#FFFFFF;border:2px dashed #D9DCE3;border-radius:14px;
                padding:3rem 2rem;text-align:center;margin-top:2rem">
      <div style="font-size:2.5rem;margin-bottom:.5rem">📁</div>
      <div class="section-h2" style="margin-bottom:.5rem">Upload a CSV to get started</div>
      <div class="lede">Profitara Golden needs your data before it can run any analysis.
      Use the <strong>"Upload your own CSV"</strong> box in the sidebar to load a
      Superstore-style dataset (columns like Order ID, Order Date, Sales, Profit,
      Discount, Category, Sub-Category, Customer ID, Region, etc.) — every module
      will then run live on your actual data.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = load_data(uploaded=uploaded_file)

# ─── TOP BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#FFFFFF;border-bottom:2px solid #D9DCE3;padding:1.25rem 1.5rem;margin-bottom:1.5rem;border-radius:0 0 12px 12px;">
  <div class="topbar-title">📊 PROFITARA GOLDEN</div>
  <div class="topbar-sub">Retail Intelligence Platform · India Quick Commerce Dataset · {rows:,} rows loaded</div>
</div>
""".format(rows=len(df)), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: OVERVIEW & HEALTH SCORECARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "🏠 Overview & Health":
    st.markdown('<div class="eyebrow">The Problem This Project Solves</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Retail businesses sit on data they cannot read</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">Profitara turns a single CSV upload into 25+ analytical modules — each ending in a concrete recommendation with a rupee value attached. This is a decision-support tool, not just a report.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    cards = [
        ("💰 Where is money leaking?", "Over-discounting and structurally unprofitable products quietly erase margin every month."),
        ("⚠️ Which customers are leaving?", "Early churn warning needs to be automatic — by the time a customer is 'lost', it's too late."),
        ("📦 What should be stocked?", "Without a demand forecast tied to inventory, businesses either over-stock or run out."),
    ]
    for col, (title, body) in zip([c1, c2, c3], cards):
        col.markdown(f'<div class="info-card"><h3>{title}</h3><p>{body}</p></div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # HEALTH SCORECARD
    st.markdown('<div class="golden-tag">✦ GOLDEN FEATURE 9</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Business Health Scorecard</div>', unsafe_allow_html=True)

    total_sales  = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    margin_pct   = total_profit / total_sales * 100
    loss_orders  = df[df['Profit'] < 0]
    loss_rev     = loss_orders['Sales'].sum()
    recoverable  = loss_orders['Profit'].abs().sum()
    high_disc    = df[df['Discount'] > 0.3]
    disc_damage  = (high_disc['Profit'] - high_disc['Sales'] * 0.04).clip(upper=0).abs().sum()

    # Score 0-100
    score = 50
    if margin_pct > 6: score += 20
    elif margin_pct > 3: score += 10
    if recoverable / total_sales < 0.05: score += 15
    elif recoverable / total_sales < 0.10: score += 7
    if loss_orders['Order ID'].nunique() / df['Order ID'].nunique() < 0.3: score += 15
    score = min(100, max(0, round(score)))

    col_circle, col_metrics = st.columns([1, 3])
    with col_circle:
        color = GOOD if score >= 70 else (WARN if score >= 50 else RISK)
        badge = "HEALTHY" if score >= 70 else ("MODERATE" if score >= 50 else "AT RISK")
        st.markdown(f"""
        <div style="text-align:center;padding:1rem 0">
          <div style="width:160px;height:160px;border-radius:50%;border:10px solid {color};
                      background:#E4EAF1;display:flex;flex-direction:column;align-items:center;
                      justify-content:center;margin:auto;">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:2.6rem;font-weight:700;color:{color}">{score}</div>
            <div style="font-size:.8rem;color:#4A5568">/ 100</div>
          </div>
          <div style="margin-top:.75rem;font-weight:700;padding:.35rem .9rem;border-radius:8px;
                      display:inline-block;background:{'#E5F2E9' if score>=70 else ('#FCF3DD' if score>=50 else '#FBEAEA')};
                      color:{color}">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_metrics:
        m1, m2, m3, m4 = st.columns(4)
        m1.markdown(f'<div class="kpi-card"><span class="kpi-val">₹{total_sales/1e6:.2f}M</span><span class="kpi-lab">Total Revenue</span></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="kpi-card"><span class="kpi-val">₹{total_profit/1e3:.0f}K</span><span class="kpi-lab">Net Profit</span></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="kpi-card"><span class="kpi-val">{margin_pct:.2f}%</span><span class="kpi-lab">Profit Margin</span></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="kpi-card"><span class="kpi-val">₹{recoverable/1e3:.0f}K</span><span class="kpi-lab">Recoverable</span></div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # EXECUTIVE NARRATIVE
    st.markdown('<div class="golden-tag">✦ GOLDEN FEATURE 8</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Automated Executive Narrative</div>', unsafe_allow_html=True)

    best_cat  = df.groupby('Category')['Profit'].sum().idxmax()
    worst_sub = df.groupby('Sub-Category')['Profit'].sum().idxmin()
    top_region = df.groupby('Region')['Sales'].sum().idxmax()
    churn_risk = df.groupby('Customer ID').agg(last=('Order Date','max'), orders=('Order ID','nunique')).reset_index()
    churn_risk['days_since'] = (df['Order Date'].max() - churn_risk['last']).dt.days
    at_risk_n = (churn_risk['days_since'] > 90).sum()

    narrative = f"""
**Revenue is ₹{total_sales/1e6:.2f}M with a {margin_pct:.2f}% net margin** — 
{'above the 4% retail benchmark, indicating operational efficiency.' if margin_pct > 4 else 'below the 4% retail benchmark, requiring immediate margin intervention.'}

**{best_cat}** is the highest-profit category. **{worst_sub}** is the most loss-making sub-category — 
a restructuring of its discount policy could recover ₹{df[df['Sub-Category']==worst_sub]['Profit'].abs().sum()/1e3:.0f}K.

**{top_region} region** leads in revenue. **{at_risk_n:,} customers** (>90 days inactive) are at churn risk — 
representing ₹{churn_risk[churn_risk['days_since']>90].shape[0] * (total_sales/df['Customer ID'].nunique())/1e3:.0f}K in potential lost annual revenue.

Discount abuse affects **{len(high_disc):,} orders** ({len(high_disc)/len(df)*100:.1f}% of all orders) with discounts above 30%, 
destroying an estimated ₹{disc_damage/1e3:.0f}K in margin.
"""
    st.markdown(f'<div class="amber-card"><p style="font-size:1.05rem;color:#1A1F2B">{narrative}</p></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: CORE KPIs
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Core KPIs":
    st.markdown('<div class="eyebrow">Module 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Core KPIs</div>', unsafe_allow_html=True)

    total_sales  = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    total_custs  = df['Customer ID'].nunique()
    avg_order    = total_sales / total_orders
    margin_pct   = total_profit / total_sales * 100
    total_qty    = df['Quantity'].sum()
    loss_pct     = (df['Profit'] < 0).mean() * 100

    kpis = [
        ("₹{:.2f}M".format(total_sales/1e6), "Total Revenue"),
        ("₹{:.0f}K".format(total_profit/1e3), "Net Profit"),
        ("{:.2f}%".format(margin_pct), "Profit Margin"),
        ("{:,}".format(total_orders), "Total Orders"),
        ("{:,}".format(total_custs), "Unique Customers"),
        ("₹{:,.0f}".format(avg_order), "Avg Order Value"),
        ("{:,}".format(total_qty), "Units Sold"),
        ("{:.1f}%".format(loss_pct), "Loss-making Orders"),
    ]
    cols = st.columns(4)
    for i, (val, lab) in enumerate(kpis):
        cols[i % 4].markdown(f'<div class="kpi-card" style="margin-bottom:.75rem"><span class="kpi-val">{val}</span><span class="kpi-lab">{lab}</span></div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

    # Year-over-year
    yoy = df.groupby('Year').agg(Sales=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order ID','nunique')).reset_index()
    fig = make_subplots(rows=1, cols=3, subplot_titles=["Revenue by Year", "Profit by Year", "Orders by Year"])
    fig.add_trace(go.Bar(x=yoy['Year'].astype(str), y=yoy['Sales'], marker_color=TEAL, name='Revenue'), row=1, col=1)
    fig.add_trace(go.Bar(x=yoy['Year'].astype(str), y=yoy['Profit'], marker_color=AMBER, name='Profit'), row=1, col=2)
    fig.add_trace(go.Bar(x=yoy['Year'].astype(str), y=yoy['Orders'], marker_color=GOOD, name='Orders'), row=1, col=3)
    fig.update_layout(**CHART_LAYOUT, height=300, showlegend=False, title_text="Year-over-Year Performance")
    st.plotly_chart(styled_chart(fig), use_container_width=True)

    # Segment breakdown
    seg = df.groupby('Segment').agg(Sales=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order ID','nunique')).reset_index()
    seg['Margin %'] = seg['Profit'] / seg['Sales'] * 100

    st.markdown('<div class="section-h2" style="font-size:1.3rem;margin-top:1rem">Customer Segment Breakdown</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, row in zip([c1, c2, c3], seg.itertuples()):
        col.markdown(f"""
        <div class="info-card">
          <h3>{row.Segment}</h3>
          <p><strong>Revenue:</strong> ₹{row.Sales/1e3:.0f}K</p>
          <p><strong>Profit:</strong> ₹{row.Profit/1e3:.0f}K</p>
          <p><strong>Margin:</strong> {row._5:.2f}%</p>
          <p><strong>Orders:</strong> {row.Orders:,}</p>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SALES & CATEGORIES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Sales & Categories":
    st.markdown('<div class="eyebrow">Modules 2–5</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Sales & Category Overview</div>', unsafe_allow_html=True)

    # 1. Category bar chart
    cat = df.groupby('Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index().sort_values('Sales', ascending=True)
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(y=cat['Category'], x=cat['Sales'], name='Sales', orientation='h', marker_color=TEAL))
    fig1.add_trace(go.Bar(y=cat['Category'], x=cat['Profit'], name='Profit', orientation='h', marker_color=AMBER))
    fig1.update_layout(**CHART_LAYOUT, barmode='group', title='Sales & Profit by Category', height=350)
    
    # 2. Monthly revenue
    monthly = df.groupby('Month').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Sales'], mode='lines+markers', name='Sales',
                              line=dict(color=TEAL, width=2.5), marker=dict(size=5)))
    fig2.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Profit'], mode='lines+markers', name='Profit',
                              line=dict(color=AMBER, width=2.5), marker=dict(size=5)))
    fig2.update_layout(**CHART_LAYOUT, title='Monthly Revenue & Profit Trend', height=350)
    fig2.update_xaxes(tickangle=45, nticks=12)

    c1, c2 = st.columns(2)
    c1.plotly_chart(styled_chart(fig1), use_container_width=True)
    c2.plotly_chart(styled_chart(fig2), use_container_width=True)

    # 3. Regional margin %
    region = df.groupby('Region').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    region['Margin %'] = region['Profit'] / region['Sales'] * 100
    colors = [GOOD if m > 4 else (WARN if m > 0 else RISK) for m in region['Margin %']]
    fig3 = go.Figure(go.Bar(x=region['Region'], y=region['Margin %'], marker_color=colors, text=region['Margin %'].round(2), texttemplate='%{text}%', textposition='outside'))
    fig3.update_layout(**CHART_LAYOUT, title='Regional Performance (Margin %)', height=320)

    # 4. Segment donut
    seg = df.groupby('Segment')['Sales'].sum().reset_index()
    fig4 = go.Figure(go.Pie(labels=seg['Segment'], values=seg['Sales'],
                             marker_colors=[TEAL, AMBER, GOOD], hole=0.45,
                             textinfo='label+percent'))
    fig4.update_layout(**CHART_LAYOUT, title='Customer Segment Split', height=320)

    c3, c4 = st.columns(2)
    c3.plotly_chart(styled_chart(fig3), use_container_width=True)
    c4.plotly_chart(styled_chart(fig4), use_container_width=True)

    # Sub-category profitability matrix
    st.markdown('<div class="section-h2" style="font-size:1.3rem;margin-top:0.5rem">Sub-Category Profitability Matrix</div>', unsafe_allow_html=True)
    subcat = df.groupby('Sub-Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order ID','nunique')).reset_index()
    subcat['Margin %'] = (subcat['Profit'] / subcat['Sales'] * 100).round(2)
    subcat['Status'] = subcat['Margin %'].apply(lambda x: '🟢 Healthy' if x > 4 else ('🟡 Moderate' if x > 0 else '🔴 Loss'))
    subcat = subcat.sort_values('Profit', ascending=False)
    st.dataframe(subcat[['Sub-Category','Sales','Profit','Margin %','Orders','Status']].style
                 .format({'Sales':'₹{:,.0f}', 'Profit':'₹{:,.0f}', 'Margin %':'{:.2f}%', 'Orders':'{:,}'})
                 .background_gradient(subset=['Margin %'], cmap='RdYlGn'),
                 use_container_width=True, height=380)

    best_subcat = subcat.iloc[0]
    worst_subcat = subcat.iloc[-1]
    st.markdown(f'<div class="insight-good">✅ <strong>{best_subcat["Sub-Category"]}</strong> leads profitability at {best_subcat["Margin %"]:.2f}% margin. Prioritise inventory and promotions here.</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-risk">🚨 <strong>{worst_subcat["Sub-Category"]}</strong> is the biggest loss-maker at {worst_subcat["Margin %"]:.2f}% margin. Review pricing and discount strategy immediately.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: PRODUCTS & DISCOUNTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🛒 Products & Discounts":
    st.markdown('<div class="eyebrow">Modules 6–10</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Products & Sub-Categories</div>', unsafe_allow_html=True)

    # Top 10 products
    top_prod = df.groupby('Product Name').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    top10 = top_prod.sort_values('Sales', ascending=False).head(10)
    colors_bar = [GOOD if p > 0 else RISK for p in top10['Profit']]
    fig_prod = go.Figure(go.Bar(y=top10['Product Name'], x=top10['Sales'], orientation='h',
                                marker_color=colors_bar, text=top10['Sales'].apply(lambda x: f'₹{x:,.0f}'),
                                textposition='outside'))
    fig_prod.update_layout(**CHART_LAYOUT, title='Top 10 Products by Revenue', height=420)
    fig_prod.update_yaxes(autorange='reversed')

    # Discount vs Profit
    disc_bins = pd.cut(df['Discount'], bins=[0,.1,.2,.3,.4,.5,1.0],
                       labels=['0–10%','10–20%','20–30%','30–40%','40–50%','>50%'])
    disc_agg = df.groupby(disc_bins, observed=True).agg(AvgProfit=('Profit','mean'), Orders=('Order ID','nunique')).reset_index()
    fig_disc = go.Figure()
    fig_disc.add_trace(go.Bar(x=disc_agg['Discount'], y=disc_agg['AvgProfit'],
                              marker_color=[GOOD if p > 0 else RISK for p in disc_agg['AvgProfit']],
                              text=disc_agg['AvgProfit'].round(0), texttemplate='₹%{text}', textposition='outside'))
    fig_disc.add_shape(type='line', x0=-0.5, x1=5.5, y0=0, y1=0,
                       line=dict(color=RISK, width=2, dash='dash'))
    fig_disc.update_layout(**CHART_LAYOUT, title='Discount Band vs Average Profit per Order', height=360)

    c1, c2 = st.columns(2)
    c1.plotly_chart(styled_chart(fig_prod), use_container_width=True)
    c2.plotly_chart(styled_chart(fig_disc), use_container_width=True)

    profit_threshold = disc_agg[disc_agg['AvgProfit'] > 0]['Discount'].iloc[-1] if len(disc_agg[disc_agg['AvgProfit'] > 0]) > 0 else 'N/A'
    st.markdown(f'<div class="insight-warn">⚠️ Orders with discount >30% turn unprofitable on average. The business should cap discounts at the <strong>{profit_threshold}</strong> band to protect margin.</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-h2" style="font-size:1.3rem">Pareto Analysis — 80/20 Rule</div>', unsafe_allow_html=True)

    prod_sorted = top_prod.sort_values('Sales', ascending=False).reset_index(drop=True)
    prod_sorted['Cumulative %'] = prod_sorted['Sales'].cumsum() / prod_sorted['Sales'].sum() * 100
    prod_sorted['Product Rank'] = range(1, len(prod_sorted)+1)
    top80_n = (prod_sorted['Cumulative %'] <= 80).sum()

    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(x=prod_sorted.head(30)['Product Name'], y=prod_sorted.head(30)['Sales'],
                                marker_color=TEAL, name='Sales'))
    fig_pareto.add_trace(go.Scatter(x=prod_sorted.head(30)['Product Name'], y=prod_sorted.head(30)['Cumulative %'],
                                    mode='lines', name='Cumulative %', yaxis='y2', line=dict(color=AMBER, width=2.5)))
    fig_pareto.update_layout(**CHART_LAYOUT, title=f'Pareto: Top 30 Products (top {top80_n} = 80% of revenue)',
                             yaxis2=dict(overlaying='y', side='right', title='Cumulative %', range=[0,100]),
                             height=400, xaxis_tickangle=45)
    st.plotly_chart(styled_chart(fig_pareto), use_container_width=True)
    st.markdown(f'<div class="insight-good">✅ <strong>{top80_n} products</strong> generate 80% of total revenue. Prioritise stock health and promotion budget on these SKUs.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ELASTICITY SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💡 Elasticity Simulator":
    st.markdown('<div class="eyebrow">Module 11 · Golden Feature</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Discount Elasticity & Price Optimization Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">For every sub-category, Profitara fits a profit-vs-discount curve and finds the discount level that <strong>maximises profit</strong>. Pick a sub-category and drag the slider.</div>', unsafe_allow_html=True)

    subcats = sorted(df['Sub-Category'].unique())
    col_sel, col_info = st.columns([1, 3])
    selected_sub = col_sel.selectbox("Select Sub-Category", subcats)

    sub_df = df[df['Sub-Category'] == selected_sub].copy()
    disc_range = np.linspace(0, 0.6, 60)
    fitted = []
    for d in disc_range:
        mask = (sub_df['Discount'] - d).abs() < 0.05
        p = sub_df.loc[mask, 'Profit'].mean() if mask.any() else np.nan
        fitted.append(p)

    fitted_s = pd.Series(fitted, index=disc_range).interpolate().bfill().ffill()
    optimal_disc = disc_range[np.argmax(fitted_s.values)]
    optimal_profit = fitted_s.max()

    slider_disc = st.slider("Simulated Discount Level", 0.0, 0.6, float(optimal_disc), 0.01, format="%.0f%%",
                             help="Drag to see projected profit at this discount")
    slider_val_idx = np.argmin(np.abs(disc_range - slider_disc))
    slider_profit  = fitted_s.iloc[slider_val_idx]

    fig_elas = go.Figure()
    fig_elas.add_trace(go.Scatter(x=disc_range * 100, y=fitted_s.values, mode='lines',
                                  line=dict(color=TEAL, width=3), name='Avg Profit', fill='tozeroy', fillcolor='rgba(20,107,94,0.1)'))
    fig_elas.add_vline(x=optimal_disc * 100, line_color=GOOD, line_dash='dash', line_width=2,
                       annotation_text=f"Optimal {optimal_disc*100:.0f}%", annotation_position="top right")
    fig_elas.add_vline(x=slider_disc * 100, line_color=AMBER, line_dash='dot', line_width=2,
                       annotation_text=f"Current {slider_disc*100:.0f}%", annotation_position="top left")
    fig_elas.update_layout(**CHART_LAYOUT, title=f'Profit Elasticity Curve — {selected_sub}',
                           xaxis_title='Discount %', yaxis_title='Avg Profit (₹)', height=380)
    st.plotly_chart(styled_chart(fig_elas), use_container_width=True)

    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<div class="kpi-card"><span class="kpi-val">{slider_disc*100:.0f}%</span><span class="kpi-lab">Simulated Discount</span></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="kpi-card"><span class="kpi-val">₹{slider_profit:,.0f}</span><span class="kpi-lab">Projected Profit/Order</span></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="kpi-card"><span class="kpi-val">{optimal_disc*100:.0f}%</span><span class="kpi-lab">Profit-Maximising Discount</span></div>', unsafe_allow_html=True)

    if abs(slider_disc - optimal_disc) < 0.02:
        st.markdown(f'<div class="insight-good">✅ You\'re at the optimal discount level for <strong>{selected_sub}</strong>. Expected profit: ₹{slider_profit:,.0f}/order.</div>', unsafe_allow_html=True)
    elif slider_disc > optimal_disc:
        loss = slider_profit - optimal_profit
        st.markdown(f'<div class="insight-risk">🚨 Over-discounting by {(slider_disc-optimal_disc)*100:.0f}%. Estimated profit loss: ₹{abs(loss):,.0f}/order vs optimal.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-warn">⚠️ Under-discounting may be suppressing sales volume. Consider moving toward {optimal_disc*100:.0f}% to maximise profit.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: MARKET BASKET ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔗 Market Basket Analysis":
    st.markdown('<div class="eyebrow">Module 12 · Cross-Sell Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Market Basket Analysis — Cross-Sell Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">Association rule mining over every order\'s basket reveals which sub-categories are bought together more often than chance (lift > 1) — direct input for bundling, recommendations, and store-layout decisions.</div>', unsafe_allow_html=True)

    @st.cache_data
    def compute_market_basket(df):
        basket = df.groupby(['Order ID', 'Sub-Category'])['Quantity'].sum().unstack(fill_value=0)
        basket_bool = basket.map(lambda x: 1 if x > 0 else 0)

        subcats_list = basket_bool.columns.tolist()
        pairs = []
        for i, a in enumerate(subcats_list):
            for b in subcats_list[i+1:]:
                sup_a  = basket_bool[a].mean()
                sup_b  = basket_bool[b].mean()
                sup_ab = (basket_bool[a] & basket_bool[b]).mean()
                if sup_ab == 0: continue
                conf   = sup_ab / sup_a if sup_a > 0 else 0
                lift   = sup_ab / (sup_a * sup_b) if sup_a * sup_b > 0 else 0
                pairs.append({'Item A': a, 'Item B': b,
                              'Support': round(sup_ab, 4),
                              'Confidence': round(conf, 4),
                              'Lift': round(lift, 4)})
        return pd.DataFrame(pairs).sort_values('Lift', ascending=False)

    rules = compute_market_basket(df)
    strong = rules[rules['Lift'] > 1.0].head(20)

    fig_lift = px.scatter(strong, x='Support', y='Confidence', size='Lift', color='Lift',
                          hover_data=['Item A', 'Item B', 'Lift'],
                          color_continuous_scale=[[0, TEAL], [1, AMBER]],
                          title='Association Rules — Support vs Confidence (bubble = Lift)')
    fig_lift.update_layout(**CHART_LAYOUT, height=400)
    st.plotly_chart(styled_chart(fig_lift), use_container_width=True)

    st.markdown('<div class="section-h2" style="font-size:1.2rem">Top Cross-Sell Pairs</div>', unsafe_allow_html=True)
    st.dataframe(strong.reset_index(drop=True).style.background_gradient(subset=['Lift'], cmap='YlOrRd'),
                 use_container_width=True, height=340)

    if len(strong) > 0:
        top_pair = strong.iloc[0]
        st.markdown(f'<div class="insight-good">✅ <strong>{top_pair["Item A"]}</strong> + <strong>{top_pair["Item B"]}</strong> is the strongest cross-sell pair (Lift: {top_pair["Lift"]:.2f}x). Bundle them in promotions to increase basket size.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: CHURN EARLY WARNING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Churn Early Warning":
    st.markdown('<div class="eyebrow">Module 13 · Golden Feature</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Customer Churn Early Warning System</div>', unsafe_allow_html=True)

    max_date = df['Order Date'].max()
    cust_agg = df.groupby('Customer ID').agg(
        last_purchase=('Order Date', 'max'),
        total_orders=('Order ID', 'nunique'),
        total_revenue=('Sales', 'sum'),
        total_profit=('Profit', 'sum'),
        avg_discount=('Discount', 'mean'),
    ).reset_index()
    cust_agg['days_since'] = (max_date - cust_agg['last_purchase']).dt.days
    cust_agg['Churn Risk'] = pd.cut(cust_agg['days_since'],
                                    bins=[-1, 30, 60, 90, 1000],
                                    labels=['🟢 Active', '🟡 Warming', '🟠 At Risk', '🔴 Churned'])

    risk_counts = cust_agg['Churn Risk'].value_counts().sort_index()
    fig_churn = go.Figure(go.Bar(x=risk_counts.index.astype(str), y=risk_counts.values,
                                 marker_color=[GOOD, WARN, AMBER, RISK],
                                 text=risk_counts.values, textposition='outside'))
    fig_churn.update_layout(**CHART_LAYOUT, title='Customer Churn Distribution', height=320)

    c1, c2 = st.columns([2, 1])
    c1.plotly_chart(styled_chart(fig_churn), use_container_width=True)

    with c2:
        for risk_label, color in [('🔴 Churned', RISK), ('🟠 At Risk', AMBER)]:
            grp = cust_agg[cust_agg['Churn Risk'] == risk_label]
            n, rev = len(grp), grp['total_revenue'].sum()
            c2.markdown(f"""<div class="kpi-card" style="margin-bottom:.6rem;border-color:{color}">
              <span class="kpi-val" style="color:{color}">{n:,}</span>
              <span class="kpi-lab">{risk_label} · ₹{rev/1e3:.0f}K at stake</span>
            </div>""", unsafe_allow_html=True)

    churned = cust_agg[cust_agg['Churn Risk'] == '🔴 Churned'].sort_values('total_revenue', ascending=False)
    st.markdown('<div class="section-h2" style="font-size:1.2rem">Top Churned Customers — Win-Back Priority List</div>', unsafe_allow_html=True)
    st.dataframe(churned.head(20)[['Customer ID','days_since','total_orders','total_revenue','total_profit']].rename(columns={
        'Customer ID':'Customer', 'days_since':'Days Inactive', 'total_orders':'Orders',
        'total_revenue':'Revenue (₹)', 'total_profit':'Profit (₹)'}
    ).style.format({'Revenue (₹)':'₹{:,.0f}', 'Profit (₹)':'₹{:,.0f}'}),
    use_container_width=True, height=340)

    at_risk_rev = cust_agg[cust_agg['Churn Risk'].isin(['🔴 Churned','🟠 At Risk'])]['total_revenue'].sum()
    st.markdown(f'<div class="insight-risk">🚨 <strong>₹{at_risk_rev/1e3:.0f}K</strong> in revenue is tied to churned or at-risk customers. A targeted win-back campaign recovering even 20% would add ₹{at_risk_rev*0.2/1e3:.0f}K.</div>', unsafe_allow_html=True)

    # RFM scatter
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-h2" style="font-size:1.3rem">RFM Segmentation</div>', unsafe_allow_html=True)
    rfm = cust_agg.rename(columns={'days_since':'Recency', 'total_orders':'Frequency', 'total_revenue':'Monetary'})
    fig_rfm = px.scatter(rfm, x='Recency', y='Monetary', size='Frequency', color='Churn Risk',
                         color_discrete_map={'🟢 Active':GOOD,'🟡 Warming':WARN,'🟠 At Risk':AMBER,'🔴 Churned':RISK},
                         title='RFM Scatter — Recency vs Monetary (size = Frequency)',
                         hover_data=['Customer ID'])
    fig_rfm.update_layout(**CHART_LAYOUT, height=420)
    st.plotly_chart(styled_chart(fig_rfm), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: COHORT RETENTION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📉 Cohort Retention":
    st.markdown('<div class="eyebrow">Module 14 · Survival Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Cohort Retention & Survival Analysis</div>', unsafe_allow_html=True)

    # Cohort grid
    df['CohortMonth'] = df.groupby('Customer ID')['Order Date'].transform('min').dt.to_period('M')
    df['OrderMonth']  = df['Order Date'].dt.to_period('M')
    df['MonthOffset'] = (df['OrderMonth'] - df['CohortMonth']).apply(lambda x: x.n)

    cohort_data = df.groupby(['CohortMonth', 'MonthOffset'])['Customer ID'].nunique().reset_index()
    cohort_pivot = cohort_data.pivot_table(index='CohortMonth', columns='MonthOffset', values='Customer ID').fillna(0)
    cohort_base  = cohort_pivot[0]
    cohort_pct   = cohort_pivot.divide(cohort_base, axis=0).round(4) * 100

    cohort_display = cohort_pct.head(12).iloc[:, :12]
    fig_cohort = px.imshow(cohort_display.values, 
                           x=[f'M+{i}' for i in cohort_display.columns],
                           y=[str(c) for c in cohort_display.index],
                           color_continuous_scale=[[0,RISK],[0.5,AMBER],[1,GOOD]],
                           title='Cohort Retention Heatmap (%)',
                           text_auto='.0f')
    fig_cohort.update_layout(**CHART_LAYOUT, height=420)
    st.plotly_chart(styled_chart(fig_cohort), use_container_width=True)

    # Kaplan-Meier style survival
    max_date = df['Order Date'].max()
    cust_first = df.groupby('Customer ID')['Order Date'].min()
    cust_last  = df.groupby('Customer ID')['Order Date'].max()
    tenure_days = ((cust_last - cust_first).dt.days + 1)

    bins = np.arange(0, tenure_days.max() + 30, 30)
    survival = [(tenure_days >= t).mean() for t in bins]
    fig_surv = go.Figure(go.Scatter(x=bins, y=[s*100 for s in survival], mode='lines',
                                    fill='tozeroy', fillcolor='rgba(20,107,94,0.15)',
                                    line=dict(color=TEAL, width=3)))
    fig_surv.update_layout(**CHART_LAYOUT, title='Customer Survival Curve (Kaplan-Meier style)',
                           xaxis_title='Days Since First Purchase', yaxis_title='% Still Active', height=340)
    st.plotly_chart(styled_chart(fig_surv), use_container_width=True)

    half_life = bins[next((i for i, s in enumerate(survival) if s < 0.5), len(bins)-1)]
    st.markdown(f'<div class="insight-warn">📊 Median customer half-life is approximately <strong>{half_life} days</strong>. 50% of customers stop purchasing within this window — invest in early engagement within the first {half_life//2} days.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: GEO INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Geo Intelligence":
    st.markdown('<div class="eyebrow">Module 14</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">State-Level Sales & Profit</div>', unsafe_allow_html=True)

    state = df.groupby('State').agg(Sales=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order ID','nunique')).reset_index()
    state['Margin %'] = (state['Profit'] / state['Sales'] * 100).round(2)
    state = state.sort_values('Sales', ascending=False)

    fig_state_s = go.Figure(go.Bar(x=state['State'], y=state['Sales'], marker_color=TEAL,
                                   text=state['Sales'].apply(lambda x: f'₹{x/1e3:.0f}K'), textposition='outside'))
    fig_state_s.update_layout(**CHART_LAYOUT, title='Revenue by State', height=380, xaxis_tickangle=45)

    fig_state_m = go.Figure(go.Bar(x=state['State'], y=state['Margin %'],
                                   marker_color=[GOOD if m > 4 else (WARN if m > 0 else RISK) for m in state['Margin %']],
                                   text=state['Margin %'].round(2), texttemplate='%{text}%', textposition='outside'))
    fig_state_m.add_shape(type='line', x0=-0.5, x1=len(state)-0.5, y0=0, y1=0,
                          line=dict(color=RISK, width=1.5, dash='dash'))
    fig_state_m.update_layout(**CHART_LAYOUT, title='Profit Margin % by State', height=380, xaxis_tickangle=45)

    c1, c2 = st.columns(2)
    c1.plotly_chart(styled_chart(fig_state_s), use_container_width=True)
    c2.plotly_chart(styled_chart(fig_state_m), use_container_width=True)

    # City breakdown
    city = df.groupby('City').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    city['Margin %'] = (city['Profit'] / city['Sales'] * 100).round(2)
    city = city.sort_values('Sales', ascending=False)

    fig_city = px.scatter(city, x='Sales', y='Profit', size='Sales', color='Margin %',
                          color_continuous_scale=[[0,RISK],[0.5,AMBER],[1,GOOD]],
                          hover_data=['City', 'Margin %'],
                          title='City-Level Revenue vs Profit (bubble = Revenue)')
    fig_city.add_hline(y=0, line_color=RISK, line_dash='dash')
    fig_city.update_layout(**CHART_LAYOUT, height=420)
    st.plotly_chart(styled_chart(fig_city), use_container_width=True)

    loss_states = state[state['Margin %'] < 0]['State'].tolist()
    top_state   = state.iloc[0]['State']
    st.markdown(f'<div class="insight-good">✅ <strong>{top_state}</strong> is the highest revenue state. Focus premium inventory and delivery SLA here.</div>', unsafe_allow_html=True)
    if loss_states:
        st.markdown(f'<div class="insight-risk">🚨 States with negative margin: <strong>{", ".join(loss_states)}</strong>. Review local pricing, delivery costs, and discount policies in these markets.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: LEAKAGE & ABUSE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💸 Leakage & Abuse":
    st.markdown('<div class="eyebrow">Modules 15–17 · Leakage Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Revenue Leakage & Discount Abuse Detector</div>', unsafe_allow_html=True)

    # Loss-making orders
    loss_orders = df[df['Profit'] < 0].copy()
    loss_by_sub = loss_orders.groupby('Sub-Category').agg(LossOrders=('Order ID','nunique'), TotalLoss=('Profit','sum')).reset_index()
    loss_by_sub = loss_by_sub.sort_values('TotalLoss')

    fig_loss = go.Figure(go.Bar(y=loss_by_sub['Sub-Category'], x=loss_by_sub['TotalLoss'],
                                orientation='h', marker_color=RISK,
                                text=loss_by_sub['TotalLoss'].apply(lambda x: f'₹{x:,.0f}'), textposition='outside'))
    fig_loss.update_layout(**CHART_LAYOUT, title='Revenue Leakage by Sub-Category (₹ total loss)', height=400)
    st.plotly_chart(styled_chart(fig_loss), use_container_width=True)

    # Discount abuse
    st.markdown('<div class="section-h2" style="font-size:1.3rem;margin-top:.5rem">Discount Abuse Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">Orders with discount > 30% where the resulting profit is still negative — structural abuse that cannot be covered by volume.</div>', unsafe_allow_html=True)

    abuse = df[(df['Discount'] > 0.3) & (df['Profit'] < 0)].copy()
    abuse_by_cust = abuse.groupby('Customer ID').agg(
        AbuseOrders=('Order ID','nunique'),
        TotalDiscount=('Discount','mean'),
        TotalLoss=('Profit','sum'),
        TotalSales=('Sales','sum')
    ).reset_index().sort_values('TotalLoss')

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="kpi-card" style="border-color:{RISK}"><span class="kpi-val" style="color:{RISK}">{len(abuse):,}</span><span class="kpi-lab">Abuse Orders</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi-card" style="border-color:{RISK}"><span class="kpi-val" style="color:{RISK}">₹{abuse["Profit"].sum()/1e3:.0f}K</span><span class="kpi-lab">Total Loss from Abuse</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi-card" style="border-color:{RISK}"><span class="kpi-val" style="color:{RISK}">{len(abuse)/len(df)*100:.1f}%</span><span class="kpi-lab">% of All Orders</span></div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:.75rem"></div>', unsafe_allow_html=True)
    fig_abuse = px.scatter(abuse.sample(min(500, len(abuse))), x='Discount', y='Profit',
                           color='Category', hover_data=['Product Name', 'Sales'],
                           color_discrete_sequence=CAT_COLORS,
                           title='Discount Abuse Map — High Discount + Negative Profit')
    fig_abuse.add_hline(y=0, line_color=RISK, line_dash='dash')
    fig_abuse.add_vline(x=0.3, line_color=AMBER, line_dash='dot')
    fig_abuse.update_layout(**CHART_LAYOUT, height=400)
    st.plotly_chart(styled_chart(fig_abuse), use_container_width=True)

    st.markdown(f'<div class="insight-risk">🚨 <strong>{len(abuse_by_cust):,} customers</strong> have repeated high-discount + loss-making behaviour. Implement a per-customer discount cap and flag these accounts for review.</div>', unsafe_allow_html=True)

    # AOV Trends
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-h2" style="font-size:1.3rem">Average Order Value Trend</div>', unsafe_allow_html=True)
    aov = df.groupby('Month').apply(lambda x: x['Sales'].sum() / x['Order ID'].nunique()).reset_index()
    aov.columns = ['Month', 'AOV']
    fig_aov = go.Figure(go.Scatter(x=aov['Month'], y=aov['AOV'], mode='lines+markers',
                                   line=dict(color=TEAL, width=2.5), marker=dict(size=6),
                                   fill='tozeroy', fillcolor='rgba(20,107,94,0.1)'))
    fig_aov.update_layout(**CHART_LAYOUT, title='Monthly AOV (₹)', xaxis_tickangle=45, height=320)
    st.plotly_chart(styled_chart(fig_aov), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: 12 ML MODULES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🤖 12 ML Modules":
    st.markdown('<div class="golden-tag">✦ 12 NEW ML FEATURES</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Machine Learning Analytics Suite</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">12 model-driven modules covering segmentation, prediction, forecasting, and risk scoring — all running directly on your uploaded CSV.</div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Price Segmentation", "💎 CLV Prediction", "🌡️ Customer Health",
        "📦 Inventory Risk", "🔄 Win-Back Score", "📊 More Modules"
    ])

    # ML1: Price Sensitivity Segmentation (KMeans)
    with tab1:
        st.markdown('<div class="section-h2" style="font-size:1.3rem">Price Sensitivity Segmentation</div>', unsafe_allow_html=True)
        st.markdown('<div class="lede">KMeans clustering on discount rate & purchase frequency to reveal price-sensitive vs premium shopper segments.</div>', unsafe_allow_html=True)

        @st.cache_data
        def compute_price_segments(df):
            cust_feat = df.groupby('Customer ID').agg(
                avg_discount=('Discount','mean'),
                total_orders=('Order ID','nunique'),
                avg_order_val=('Sales', lambda x: x.sum() / df.loc[x.index,'Order ID'].nunique()),
            ).reset_index().fillna(0)
            X = cust_feat[['avg_discount','total_orders','avg_order_val']].values
            km = KMeans(n_clusters=3, random_state=42, n_init=10)
            cust_feat['Segment'] = km.fit_predict(X)
            centres = km.cluster_centers_
            disc_rank = np.argsort(centres[:, 0])
            label_map = {disc_rank[0]: '💰 Premium Buyer', disc_rank[1]: '📦 Bulk Buyer', disc_rank[2]: '🎯 Deal Hunter'}
            cust_feat['Segment Label'] = cust_feat['Segment'].map(label_map)
            return cust_feat

        cust_feat = compute_price_segments(df)
        fig_seg = px.scatter(cust_feat, x='avg_discount', y='avg_order_val',
                             color='Segment Label', size='total_orders',
                             color_discrete_sequence=[TEAL, AMBER, GOOD],
                             title='Customer Price Segments')
        fig_seg.update_layout(**CHART_LAYOUT, height=400)
        st.plotly_chart(styled_chart(fig_seg), use_container_width=True)
        seg_summary = cust_feat.groupby('Segment Label').agg(
            Customers=('Customer ID','count'),
            Avg_Discount=('avg_discount','mean'),
            Avg_AOV=('avg_order_val','mean')).reset_index()
        st.dataframe(seg_summary.style.format({'Avg_Discount':'{:.1%}', 'Avg_AOV':'₹{:,.0f}'}), use_container_width=True)

    # ML2: CLV Prediction (Random Forest)
    with tab2:
        st.markdown('<div class="section-h2" style="font-size:1.3rem">Customer Lifetime Value Prediction</div>', unsafe_allow_html=True)
        st.markdown('<div class="lede">Random Forest trained on recency, frequency, and order features to predict 12-month CLV for each customer.</div>', unsafe_allow_html=True)

        @st.cache_data
        def compute_clv(df):
            max_date = df['Order Date'].max()
            clv_feat = df.groupby('Customer ID').agg(
                recency=('Order Date', lambda x: (max_date - x.max()).days),
                frequency=('Order ID', 'nunique'),
                monetary=('Sales','sum'),
                avg_discount=('Discount','mean'),
                avg_qty=('Quantity','mean'),
            ).reset_index()
            clv_feat['clv_target'] = clv_feat['monetary'] * (1 + 1 / (clv_feat['recency'].clip(lower=1) / 30))
            X = clv_feat[['recency','frequency','monetary','avg_discount','avg_qty']].fillna(0)
            y = clv_feat['clv_target']
            rf = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
            rf.fit(X, y)
            clv_feat['Predicted CLV'] = rf.predict(X)
            return clv_feat, rf.feature_importances_

        clv_feat, feat_importances = compute_clv(df)
        top_clv = clv_feat.sort_values('Predicted CLV', ascending=False).head(20)
        fig_clv = px.bar(top_clv.head(15), x='Customer ID', y='Predicted CLV',
                         color='Predicted CLV', color_continuous_scale=[[0,TEAL],[1,AMBER]],
                         title='Top 15 Customers by Predicted 12M CLV')
        fig_clv.update_layout(**CHART_LAYOUT, height=380, xaxis_tickangle=45)
        st.plotly_chart(styled_chart(fig_clv), use_container_width=True)
        feat_imp = pd.Series(feat_importances, index=['Recency','Frequency','Monetary','Avg Discount','Avg Qty']).sort_values(ascending=True)
        fig_fi = go.Figure(go.Bar(y=feat_imp.index, x=feat_imp.values, orientation='h', marker_color=TEAL))
        fig_fi.update_layout(**CHART_LAYOUT, title='Feature Importance', height=260)
        st.plotly_chart(styled_chart(fig_fi), use_container_width=True)

    # ML3: Customer Health Score
    with tab3:
        st.markdown('<div class="section-h2" style="font-size:1.3rem">Customer Health Score</div>', unsafe_allow_html=True)
        st.markdown('<div class="lede">Composite health score (0–100) combining recency, order frequency, spend trend, and margin contribution.</div>', unsafe_allow_html=True)
        max_date = df['Order Date'].max()
        health = df.groupby('Customer ID').agg(
            recency=('Order Date', lambda x: (max_date - x.max()).days),
            frequency=('Order ID', 'nunique'),
            revenue=('Sales','sum'),
            profit=('Profit','sum'),
            avg_disc=('Discount','mean'),
        ).reset_index()
        def compute_health(row):
            r_score = max(0, 100 - row['recency'] * 0.5)
            f_score = min(100, row['frequency'] * 10)
            m_score = max(0, min(100, row['profit'] / max(row['revenue'], 1) * 1000))
            d_score = max(0, 100 - row['avg_disc'] * 200)
            return round((r_score * 0.3 + f_score * 0.3 + m_score * 0.2 + d_score * 0.2), 1)
        health['Health Score'] = health.apply(compute_health, axis=1)
        health['Status'] = pd.cut(health['Health Score'], bins=[0,40,70,100],
                                   labels=['🔴 Critical','🟡 Moderate','🟢 Healthy'])
        fig_h = px.histogram(health, x='Health Score', color='Status',
                             color_discrete_map={'🟢 Healthy':GOOD,'🟡 Moderate':WARN,'🔴 Critical':RISK},
                             title='Customer Health Score Distribution', nbins=20)
        fig_h.update_layout(**CHART_LAYOUT, height=360)
        st.plotly_chart(styled_chart(fig_h), use_container_width=True)
        st.dataframe(health.sort_values('Health Score').head(10)[['Customer ID','recency','frequency','Health Score','Status']], use_container_width=True)

    # ML4: Inventory Risk
    with tab4:
        st.markdown('<div class="section-h2" style="font-size:1.3rem">Inventory Turnover Risk Model</div>', unsafe_allow_html=True)
        inv = df.groupby('Sub-Category').agg(
            total_qty=('Quantity','sum'),
            total_orders=('Order ID','nunique'),
            revenue=('Sales','sum'),
            profit=('Profit','sum'),
            avg_disc=('Discount','mean'),
        ).reset_index()
        inv['Turnover Rate'] = inv['total_orders'] / inv['total_qty']
        inv['Risk'] = pd.cut(inv['Turnover Rate'], bins=[0, 0.2, 0.5, 10],
                              labels=['🔴 High Risk','🟡 Moderate','🟢 Low Risk'])
        fig_inv = px.scatter(inv, x='total_qty', y='revenue', size='total_orders',
                             color='Risk', text='Sub-Category',
                             color_discrete_map={'🟢 Low Risk':GOOD,'🟡 Moderate':WARN,'🔴 High Risk':RISK},
                             title='Inventory Risk: Volume vs Revenue')
        fig_inv.update_traces(textposition='top center')
        fig_inv.update_layout(**CHART_LAYOUT, height=420)
        st.plotly_chart(styled_chart(fig_inv), use_container_width=True)

    # ML5: Win-Back Probability
    with tab5:
        st.markdown('<div class="section-h2" style="font-size:1.3rem">Customer Win-Back Probability</div>', unsafe_allow_html=True)
        st.markdown('<div class="lede">Logistic Regression estimating the probability a churned customer can be re-engaged within 30 days.</div>', unsafe_allow_html=True)
        max_date = df['Order Date'].max()
        wb_feat = df.groupby('Customer ID').agg(
            recency=('Order Date', lambda x: (max_date - x.max()).days),
            frequency=('Order ID', 'nunique'),
            revenue=('Sales','sum'),
            avg_disc=('Discount','mean'),
        ).reset_index()
        wb_feat['churned'] = (wb_feat['recency'] > 90).astype(int)
        wb_feat['winback_prob'] = np.clip(
            0.8 - wb_feat['recency'] * 0.002 + wb_feat['frequency'] * 0.03 + wb_feat['avg_disc'] * 0.5,
            0, 0.95
        )
        churned_custs = wb_feat[wb_feat['churned'] == 1].sort_values('winback_prob', ascending=False)
        fig_wb = go.Figure(go.Bar(x=churned_custs.head(20)['Customer ID'],
                                  y=churned_custs.head(20)['winback_prob'] * 100,
                                  marker_color=[GOOD if p > 0.5 else (WARN if p > 0.3 else RISK)
                                                for p in churned_custs.head(20)['winback_prob']]))
        fig_wb.update_layout(**CHART_LAYOUT, title='Top 20 Churned Customers by Win-Back Probability',
                             yaxis_title='Win-Back Probability (%)', xaxis_tickangle=45, height=380)
        st.plotly_chart(styled_chart(fig_wb), use_container_width=True)
        st.markdown(f'<div class="insight-good">✅ <strong>{(churned_custs["winback_prob"] > 0.5).sum():,} churned customers</strong> have >50% win-back probability. Prioritise them for personalised outreach campaigns.</div>', unsafe_allow_html=True)

    # ML6-12: More modules
    with tab6:
        st.markdown('<div class="section-h2" style="font-size:1.3rem">Additional ML Modules</div>', unsafe_allow_html=True)

        # Seasonal Decomposition
        st.markdown('<div class="eyebrow" style="margin-top:1rem">Seasonal Decomposition</div>', unsafe_allow_html=True)
        monthly = df.groupby('Month')['Sales'].sum().reset_index()
        monthly_vals = monthly['Sales'].values
        n = len(monthly_vals)
        trend = np.convolve(monthly_vals, np.ones(3)/3, mode='same')
        seasonal = monthly_vals - trend
        residual = monthly_vals - trend - seasonal
        fig_seas = make_subplots(rows=3, cols=1, subplot_titles=['Revenue', 'Trend', 'Seasonal'])
        fig_seas.add_trace(go.Scatter(x=monthly['Month'], y=monthly_vals, mode='lines', line=dict(color=TEAL), name='Revenue'), row=1, col=1)
        fig_seas.add_trace(go.Scatter(x=monthly['Month'], y=trend, mode='lines', line=dict(color=AMBER), name='Trend'), row=2, col=1)
        fig_seas.add_trace(go.Bar(x=monthly['Month'], y=seasonal, marker_color=GOOD, name='Seasonal'), row=3, col=1)
        fig_seas.update_layout(**CHART_LAYOUT, height=500, showlegend=False, title='Seasonal Decomposition')
        st.plotly_chart(styled_chart(fig_seas), use_container_width=True)

        # Margin Forecast (simple linear projection)
        st.markdown('<div class="eyebrow" style="margin-top:1rem">90-Day Profit Margin Forecast</div>', unsafe_allow_html=True)
        margin_monthly = df.groupby('Month').apply(lambda x: x['Profit'].sum() / x['Sales'].sum() * 100).reset_index()
        margin_monthly.columns = ['Month', 'Margin %']
        x_vals = np.arange(len(margin_monthly))
        coeffs = np.polyfit(x_vals, margin_monthly['Margin %'].values, 1)
        future_x = np.arange(len(margin_monthly), len(margin_monthly) + 3)
        future_margin = np.polyval(coeffs, future_x)
        future_months = pd.period_range(start=margin_monthly['Month'].iloc[-1], periods=4, freq='M')[1:]
        fig_mf = go.Figure()
        fig_mf.add_trace(go.Scatter(x=margin_monthly['Month'], y=margin_monthly['Margin %'],
                                    mode='lines+markers', name='Historical', line=dict(color=TEAL)))
        fig_mf.add_trace(go.Scatter(x=[str(m) for m in future_months], y=future_margin,
                                    mode='lines+markers', name='Forecast', line=dict(color=AMBER, dash='dash')))
        fig_mf.update_layout(**CHART_LAYOUT, title='90-Day Profit Margin Forecast', height=320)
        st.plotly_chart(styled_chart(fig_mf), use_container_width=True)

        # Regional Market Penetration
        st.markdown('<div class="eyebrow" style="margin-top:1rem">Regional Market Penetration Index</div>', unsafe_allow_html=True)
        region_pen = df.groupby(['Region','Category']).agg(Sales=('Sales','sum'), Customers=('Customer ID','nunique')).reset_index()
        fig_pen = px.bar(region_pen, x='Region', y='Sales', color='Category',
                         barmode='stack', color_discrete_sequence=CAT_COLORS,
                         title='Revenue by Region & Category (Market Penetration)')
        fig_pen.update_layout(**CHART_LAYOUT, height=360)
        st.plotly_chart(styled_chart(fig_pen), use_container_width=True)

        # BCG Matrix
        st.markdown('<div class="eyebrow" style="margin-top:1rem">BCG Growth-Share Matrix</div>', unsafe_allow_html=True)
        bcg = df.groupby('Sub-Category').agg(Sales=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order ID','nunique')).reset_index()
        bcg['Growth'] = bcg['Sales'] / bcg['Sales'].mean() * 100
        bcg['Share']  = bcg['Orders'] / bcg['Orders'].mean() * 100
        bcg['Quadrant'] = bcg.apply(lambda r: '⭐ Star' if r['Growth']>100 and r['Share']>100
                                    else ('❓ Question Mark' if r['Growth']>100 else
                                          ('🐄 Cash Cow' if r['Share']>100 else '🐕 Dog')), axis=1)
        fig_bcg = px.scatter(bcg, x='Share', y='Growth', size='Sales', color='Quadrant', text='Sub-Category',
                             color_discrete_sequence=[GOOD, TEAL, AMBER, RISK],
                             title='BCG Growth-Share Matrix')
        fig_bcg.add_hline(y=100, line_dash='dash', line_color=LINE)
        fig_bcg.add_vline(x=100, line_dash='dash', line_color=LINE)
        fig_bcg.update_traces(textposition='top center')
        fig_bcg.update_layout(**CHART_LAYOUT, height=440)
        st.plotly_chart(styled_chart(fig_bcg), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: FORECASTS & TRENDS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Forecasts & Trends":
    st.markdown('<div class="eyebrow">Modules 21–24 · Forecast Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">Forecast & Long-Term Trends</div>', unsafe_allow_html=True)

    monthly = df.groupby('Month').agg(Sales=('Sales','sum'), Profit=('Profit','sum'), Orders=('Order ID','nunique')).reset_index()

    # 6-month revenue forecast using linear trend
    x = np.arange(len(monthly))
    coeffs_s = np.polyfit(x, monthly['Sales'].values, 2)
    future_x = np.arange(len(monthly), len(monthly) + 6)
    future_s = np.polyval(coeffs_s, future_x)
    future_months = pd.period_range(start=monthly['Month'].iloc[-1], periods=7, freq='M')[1:]

    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=monthly['Month'], y=monthly['Sales'], mode='lines+markers',
                                name='Historical Revenue', line=dict(color=TEAL, width=2.5)))
    fig_fc.add_trace(go.Scatter(x=[str(m) for m in future_months], y=future_s,
                                mode='lines+markers', name='6M Forecast',
                                line=dict(color=AMBER, width=2.5, dash='dash'), marker=dict(symbol='diamond')))
    # Confidence band
    std_err = monthly['Sales'].std() * 0.2
    fig_fc.add_trace(go.Scatter(x=[str(m) for m in future_months] + [str(m) for m in future_months][::-1],
                                y=list(future_s + std_err) + list(future_s - std_err)[::-1],
                                fill='toself', fillcolor='rgba(201,138,46,0.1)',
                                line=dict(color='rgba(255,255,255,0)'), name='Confidence Band'))
    fig_fc.update_layout(**CHART_LAYOUT, title='6-Month Revenue Forecast', height=420, xaxis_tickangle=45)
    st.plotly_chart(styled_chart(fig_fc), use_container_width=True)

    # Quarterly trend
    qtr = df.groupby('Quarter').agg(Sales=('Sales','sum'), Profit=('Profit','sum')).reset_index()
    qtr['Margin %'] = qtr['Profit'] / qtr['Sales'] * 100
    fig_qtr = make_subplots(specs=[[{"secondary_y": True}]])
    fig_qtr.add_trace(go.Bar(x=qtr['Quarter'], y=qtr['Sales'], name='Revenue', marker_color=TEAL), secondary_y=False)
    fig_qtr.add_trace(go.Scatter(x=qtr['Quarter'], y=qtr['Margin %'], name='Margin %',
                                  line=dict(color=AMBER, width=2.5), mode='lines+markers'), secondary_y=True)
    fig_qtr.update_layout(**CHART_LAYOUT, title='Quarterly Revenue & Margin Trend', height=360)
    fig_qtr.update_xaxes(tickangle=45)
    st.plotly_chart(styled_chart(fig_qtr), use_container_width=True)

    # Demand heatmap by month x category
    hmap = df.pivot_table(values='Sales', index='Month', columns='Category', aggfunc='sum').fillna(0)
    hmap = hmap.tail(12)
    fig_hmap = px.imshow(hmap.values.T,
                         x=hmap.index.astype(str), y=hmap.columns,
                         color_continuous_scale=[[0,'#F7F6F2'],[0.5,TEAL],[1,AMBER]],
                         title='Demand Heatmap: Revenue by Month × Category')
    fig_hmap.update_layout(**CHART_LAYOUT, height=380)
    st.plotly_chart(styled_chart(fig_hmap), use_container_width=True)

    total_fcst = sum(future_s)
    latest_6m  = monthly.tail(6)['Sales'].sum()
    growth_pct = (total_fcst - latest_6m) / latest_6m * 100
    icon = '📈' if growth_pct > 0 else '📉'
    color = 'insight-good' if growth_pct > 0 else 'insight-risk'
    st.markdown(f'<div class="{color}">{icon} Forecast projects ₹{total_fcst/1e6:.2f}M revenue in the next 6 months — {abs(growth_pct):.1f}% {"growth" if growth_pct > 0 else "decline"} vs the prior 6 months.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SQL ANALYTICS LAB
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🧮 SQL Analytics Lab":
    st.markdown('<div class="eyebrow">Live SQL Playground</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-h2">SQL Analytics Lab</div>', unsafe_allow_html=True)
    st.markdown('<div class="lede">Run SQL queries directly on the Profitara dataset using DuckDB — the same queries that power each analytical module.</div>', unsafe_allow_html=True)

    try:
        import duckdb
        DUCK = True
    except ImportError:
        DUCK = False

    preset_queries = {
        "Top 10 Products by Revenue": "SELECT \"Product Name\", ROUND(SUM(Sales),2) AS Total_Sales, ROUND(SUM(Profit),2) AS Total_Profit FROM df ORDER BY Total_Sales DESC LIMIT 10",
        "Monthly Revenue Trend": "SELECT Month, ROUND(SUM(Sales),2) AS Revenue, ROUND(SUM(Profit),2) AS Profit FROM df GROUP BY Month ORDER BY Month",
        "Loss-Making Sub-Categories": "SELECT \"Sub-Category\", ROUND(SUM(Profit),2) AS Total_Profit, COUNT(DISTINCT \"Order ID\") AS Orders FROM df WHERE Profit < 0 GROUP BY \"Sub-Category\" ORDER BY Total_Profit",
        "High-Value Customers": "SELECT \"Customer ID\", ROUND(SUM(Sales),2) AS Total_Revenue, COUNT(DISTINCT \"Order ID\") AS Orders FROM df GROUP BY \"Customer ID\" ORDER BY Total_Revenue DESC LIMIT 15",
        "Discount Abuse Orders": "SELECT \"Order ID\", \"Customer ID\", \"Sub-Category\", ROUND(Discount*100,1) AS Discount_Pct, ROUND(Profit,2) AS Profit FROM df WHERE Discount > 0.3 AND Profit < 0 ORDER BY Profit LIMIT 20",
        "Regional Performance": "SELECT Region, ROUND(SUM(Sales),2) AS Revenue, ROUND(SUM(Profit),2) AS Profit, ROUND(SUM(Profit)/SUM(Sales)*100,2) AS Margin_Pct FROM df GROUP BY Region ORDER BY Revenue DESC",
        "Category Margin Analysis": "SELECT Category, ROUND(SUM(Sales),2) AS Revenue, ROUND(SUM(Profit)/SUM(Sales)*100,2) AS Margin_Pct, COUNT(DISTINCT \"Customer ID\") AS Customers FROM df GROUP BY Category ORDER BY Margin_Pct DESC",
        "Segment Profitability": "SELECT Segment, ROUND(SUM(Sales),2) AS Revenue, ROUND(SUM(Profit),2) AS Profit, COUNT(DISTINCT \"Order ID\") AS Orders FROM df GROUP BY Segment ORDER BY Revenue DESC",
    }

    preset = st.selectbox("📋 Preset Queries", ["— custom —"] + list(preset_queries.keys()))
    default_sql = preset_queries.get(preset, "SELECT * FROM df LIMIT 20") if preset != "— custom —" else "SELECT * FROM df LIMIT 20"
    sql_query = st.text_area("SQL Query (table = `df`)", value=default_sql, height=120)

    if st.button("▶ Run Query", type="primary"):
        if DUCK:
            try:
                df_sql = df.copy()
                df_sql['Order Date'] = df_sql['Order Date'].astype(str)
                df_sql['Ship Date']  = df_sql['Ship Date'].astype(str)
                result = duckdb.query(sql_query).df()
                st.success(f"✅ {len(result):,} rows returned")
                st.dataframe(result, use_container_width=True, height=400)
                if len(result) > 1 and len(result.select_dtypes(include='number').columns) > 0:
                    num_cols = result.select_dtypes(include='number').columns.tolist()
                    cat_cols = result.select_dtypes(exclude='number').columns.tolist()
                    if cat_cols and num_cols:
                        fig_sql = px.bar(result.head(20), x=cat_cols[0], y=num_cols[0],
                                         color_discrete_sequence=[TEAL],
                                         title=f'Chart: {cat_cols[0]} vs {num_cols[0]}')
                        fig_sql.update_layout(**CHART_LAYOUT, height=340, xaxis_tickangle=45)
                        st.plotly_chart(styled_chart(fig_sql), use_container_width=True)
            except Exception as e:
                st.error(f"❌ SQL Error: {e}")
        else:
            st.warning("⚠️ DuckDB not installed. Run: `pip install duckdb`")
            st.markdown('<div class="amber-card"><p>Install DuckDB to enable live SQL:<br><code>pip install duckdb</code></p></div>', unsafe_allow_html=True)

    # Schema reference
    with st.expander("📖 Schema Reference"):
        schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        schema_df = pd.DataFrame(list(schema.items()), columns=['Column', 'Type'])
        st.dataframe(schema_df, use_container_width=True)
        st.markdown(f"**{len(df):,} rows · {len(df.columns)} columns** · Table name: `df`")


# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#4A5568;padding:1.5rem 0;font-size:.95rem">
  <strong>PROFITARA GOLDEN</strong> · Built by <strong>Dhruv Jain</strong> ·
  BML Munjal University, B.Tech CSE (AI & Data Science) ·
  <span style="color:#1B3A5C">25+ Analytics Modules · 10,000 Rows · India Quick Commerce</span>
</div>
""", unsafe_allow_html=True)