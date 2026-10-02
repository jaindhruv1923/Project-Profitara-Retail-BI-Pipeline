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

### Phase 2: CLV Done Properly (In Progress)
- [ ] Time-based split: features in observation window, spend in prediction window.
- [ ] Baselines: Mean spend, Linear Regression, BG/NBD + Gamma-Gamma.
- [ ] Tree models: Random Forest, HistGradientBoosting.
- [ ] Bootstrap 95% confidence intervals, decile calibration, SHAP feature importance.
- [ ] Record honest numbers.

---

## Decisions & Observations
- Will be logged as audit proceeds.

## Verified Numbers
- (To be populated from code runs during Audit & Phases)
