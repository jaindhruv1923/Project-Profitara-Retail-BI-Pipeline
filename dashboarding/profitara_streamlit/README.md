# PROFITARA GOLDEN — Streamlit Dashboard

**Built by Dhruv Sharma · BML Munjal University · B.Tech CSE (AI & Data Science)**

---

## 🚀 How to Run (Super Easy)

### Option 1 — Windows
Double-click `run.bat`

### Option 2 — Mac/Linux
```bash
chmod +x run.sh
./run.sh
```

### Option 3 — Manual
```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 Files
```
profitara_streamlit/
├── app.py                        ← Main Streamlit dashboard (all 13 pages)
├── Profitara_India_Dataset.csv   ← Dataset (10,000 rows)
├── requirements.txt              ← Python dependencies
├── run.sh                        ← Mac/Linux launcher
├── run.bat                       ← Windows launcher
└── README.md                     ← This file
```

---

## 📊 13 Dashboard Pages

| Page | Modules |
|------|---------|
| 🏠 Overview & Health | Business Health Scorecard (0–100) + Executive Narrative |
| 📊 Core KPIs | 8 KPIs, YoY trends, segment breakdown |
| 📈 Sales & Categories | Category charts, monthly trend, regional margin, segment donut |
| 🛒 Products & Discounts | Top 10 products, discount band analysis, Pareto 80/20 |
| 💡 Elasticity Simulator | Interactive discount optimizer per sub-category |
| 🔗 Market Basket Analysis | Apriori association rules, lift scatter, cross-sell table |
| ⚠️ Churn Early Warning | RFM segmentation, churn distribution, win-back priority list |
| 📉 Cohort Retention | Cohort heatmap + Kaplan-Meier survival curve |
| 🗺️ Geo Intelligence | State & city-level sales, margin maps |
| 💸 Leakage & Abuse | Revenue leakage, discount abuse detector, AOV trend |
| 🤖 12 ML Modules | KMeans segmentation, Random Forest CLV, Logistic win-back, BCG, seasonal decomp |
| 🔮 Forecasts & Trends | 6M revenue forecast, quarterly trend, demand heatmap |
| 🧮 SQL Analytics Lab | Live DuckDB SQL on the dataset + preset queries |

---

## 🎨 Design
Matches the HTML dashboard exactly:
- **Fonts:** Atkinson Hyperlegible + IBM Plex Mono  
- **Colors:** Teal `#146B5E` · Amber `#C98A2E` · Paper `#FAF8F4`
- **Cards, badges, insight boxes** — same as HTML version
- **Upload your own CSV** via sidebar to re-run all modules on your data
