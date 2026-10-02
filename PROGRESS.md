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

### Phase 0: Truth Cleanup (In Progress)
- [ ] Initialize `CLAIMS_LEDGER.csv`.
- [ ] Generate `GITHUB_PROFILE_README_FIXES.md`.
- [ ] Fix conflicting claims in existing documentation.
- [ ] Commit Phase 0 changes.

---

## Decisions & Observations
- Will be logged as audit proceeds.

## Verified Numbers
- (To be populated from code runs during Audit & Phases)
