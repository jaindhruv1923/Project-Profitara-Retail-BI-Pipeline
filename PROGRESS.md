# PROGRESS: Profitara Audit and Upgrade

> Note: This repository was initialized locally on branch `upgrade` from the original unversioned project files. History must be rebased onto a fresh clone before publishing to GitHub. `main` branch preserves the exact original state.

## Current Status
- **Current Phase**: Step 1 - Audit (Read-only)
- **Branch**: `upgrade`
- **Last Updated**: 2026-10-02

---

## Progress Log

### Step 0: Setup
- [x] Initialized git repo on `main` branch.
- [x] Committed untouched original state (`2c244f1`).
- [x] Created and checked out `upgrade` branch.
- [x] Created `PROGRESS.md`.

### Step 1: Audit (Completed)
- [x] Inspected dataset `01_Dataset/Profitara_India_Dataset.csv`: Confirmed synthetic nature (Gurugram 680 random PIN codes, 9,950 product IDs for 66 names, linear discount-margin decay).
- [x] Inspected ML notebook `04_ML_Pipeline/Profitara_ML_Pipeline.ipynb`: Identified target leakage in CLV ($R^2=0.930$, `Monetary = Frequency * AvgOrderValue`), circular churn definition (`Recency > 75th percentile`, AUC=0.91), degenerate K-Means ($k=2$, silhouette=0.611).
- [x] Inspected SQL file `03_SQL/Profitara_Complete.sql`: Discovered it contains 9,994 rows of US Superstore data in USD, not the Indian dataset.
- [x] Inspected documentation (`README.md`, `07_BA_Documentation/*`, `02_Excel_Workbook`, `06_Standalone_HTML_Dashboard`): Found extensive mismatches between USD/Superstore and INR/Indian quick-commerce.
- [x] Evaluated resume claims against verified outputs.
- [x] Wrote `AUDIT.md` and `UPGRADE_PLAN.md`.

### Phase 0: Truth Cleanup (Completed)
- [x] Initialized `CLAIMS_LEDGER.csv`.
- [x] Generated `GITHUB_PROFILE_README_FIXES.md`.
- [x] Fixed conflicting claims in existing documentation and Power BI README.
- [x] Committed Phase 0 changes (`e096638`).

### Phase 1: Data Honesty (Completed)
- [x] Created `scripts/download_real_data.py`.
- [x] Configured `.gitignore` for real data directory and databases.
- [x] Successfully downloaded real UCI Online Retail dataset (541,909 rows, 4,372 customers) into `data/real/online_retail_II.csv`.
- [x] Stated plainly in `README.md` the dual-dataset design: synthetic Indian quick-commerce for UI storytelling, real UCI dataset for ML core.
- [x] Committed Phase 1 changes.

### Phase 2: CLV Done Properly (Completed)
- [x] Implemented time-based split: 9-month observation window vs 90-day prediction window on real UCI retail dataset.
- [x] Zero target leakage: Target is future 90-day spend (£914.25 mean); features strictly historical.
- [x] Benchmarked Predict Mean (R² -0.001, MAE £1200.44), Linear Regression (R² 0.088, MAE £787.94), BG/NBD + Gamma-Gamma (R² 0.082, MAE £755.28), Random Forest (R² 0.091, MAE £815.33), Gradient Boosting (R² 0.093, MAE £811.88).
- [x] Generated 95% bootstrap confidence intervals for R² and MAE.
- [x] Computed 10-decile calibration (Decile 10 predicted £4,329.79 vs actual £4,095.44).
- [x] Computed permutation feature importance showing historical monetary spend (+£183.12 MAE) and frequency (+£136.34 MAE) as top drivers.
- [x] Exported benchmarks to `reports/clv_model_benchmarks.csv` and figures.
- [x] Committed Phase 2 changes.

### Phase 3: Churn as a Decision (Completed)
- [x] Defined non-contractual churn strictly out-of-time: 0 purchases in future 90 days (41.2% churn base rate).
- [x] Built and trained calibrated Logistic Regression model (ROC-AUC 0.764, 95% CI: [0.736, 0.793], Brier score 0.1928, Log-Loss 0.5611).
- [x] Defined Expected Value decision framework: EV = P(churn) * response_rate * predicted_CLV * margin - campaign_cost.
- [x] Saved assumptions in `config/business_assumptions.yaml` (£5 cost, 20% margin, 15% response rate, £1,500 budget).
- [x] Backtested against naive policies: Proposed EV policy achieves +£720.03 simulated net value, outperforming Top Recency (+£31.60), Top Spender (+£261.47), and Random (-£19.19).
- [x] Generated sensitivity analysis matrix across cost (£2.50 to £10.00) and response rates (5% to 25%).
- [x] Committed Phase 3 changes.

### Phase 4: Segmentation & Basket Analysis (Completed)
- [x] Evaluated K-Means across k in 2..7 using inertia, silhouette score, and stability across 5 seeds (42, 100, 2024, 7, 999).
- [x] Justified k=4 for operational business segmentation (seed stability 0.947, silhouette 0.330).
- [x] Profiled 4 actionable customer segments: Champions & VIPs (702 customers, 64.2% revenue share), Loyal & Steady Buyers (1,182 customers, 24.5% revenue), At-Risk Spenders (875 customers, 4.9% revenue), Hibernating Inactive (1,575 customers, 6.5% revenue).
- [x] Mapped each segment to actionable CRM retention/loyalty strategies in `reports/customer_segment_profiles.csv`.
- [x] Executed Apriori market basket analysis on real retail transactions (17,512 baskets). Discovered 493 itemsets and 248 association rules at min_support=0.015 and min_lift=1.2.
- [x] Top cross-sell rule: Wooden Star Christmas ===> Wooden Heart Christmas (Lift 27.865, Confidence 73.7%).
- [x] Exported surviving rules to `reports/apriori_surviving_rules.csv` and charts.
- [x] Committed Phase 4 changes.

### Phase 5: Forecasting (In Progress)
- [ ] Aggregate real retail time series to weekly/monthly frequency.
- [ ] Implement rolling-origin backtest (walk-forward CV across 3 folds).
- [ ] Benchmark: Seasonal Naive baseline, Holt-Winters exponential smoothing, Autoregressive ML model (Random Forest / Ridge with lag features).
- [ ] Report honest performance across folds (RMSE & MAPE), explicitly identifying where naive wins or loses.

---

## Decisions & Observations
- Will be logged as audit proceeds.

## Verified Numbers
- (To be populated from code runs during Audit & Phases)
