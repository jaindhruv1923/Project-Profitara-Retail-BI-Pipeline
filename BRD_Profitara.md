# Business Requirements Document (BRD)
## Profitara — Retail Business Intelligence Platform

**Prepared by:** Dhruv Jain
**Document type:** Business Requirements Document
**Status:** Retrospective BRD — documented against a completed build, framed as it would have been scoped at project kickoff

---

### 1. Purpose

This document defines the business problem, requirements, and success criteria for Profitara, a retail analytics platform built on a 10,000-row India quick-commerce transaction dataset (4,918 orders, 1,448 customers, 9 categories, 17 sub-categories, ₹66.95L total revenue).

### 2. Business Problem

Retail businesses generate large volumes of transaction data but lack the tooling to convert it into decisions. Three problems drove this project:

| Problem | Business impact if unaddressed |
|---|---|
| No visibility into where margin is leaking | Discount overuse and structurally unprofitable products quietly erode profit every month |
| No early warning for customer churn | By the time a customer is confirmed "lost," win-back is far more expensive than retention |
| No demand signal tied to inventory or pricing decisions | Businesses over-stock or run out, and pricing/discount decisions are made on gut feel |

### 3. Stakeholders

| Stakeholder (role-based, hypothetical for this exercise) | Interest |
|---|---|
| Retail Operations Lead | Wants a single view of business health, updated automatically |
| Marketing / CRM team | Needs a ranked list of at-risk customers and the revenue tied to them, to prioritize win-back spend |
| Pricing / Category team | Needs to know which sub-categories are over-discounted and what discount level actually maximizes profit |
| Finance | Needs revenue, margin, and leakage figures traceable back to source transactions |

### 4. Scope

**In scope:**
- Descriptive analytics (revenue, margin, category/segment performance)
- Predictive analytics (churn probability, 12-month CLV, demand forecast)
- Prescriptive analytics (discount optimization, win-back prioritization, cross-sell recommendations)
- A self-service SQL layer for ad-hoc business questions

**Out of scope (documented for transparency, not built):**
- Real-time transaction ingestion (project uses a static/batch dataset)
- Multi-tenant deployment for more than one retail business
- Automated execution of recommendations (e.g. auto-applying a discount change)

### 5. Business Requirements

| ID | Requirement | Delivered as |
|---|---|---|
| BR-01 | Show overall business health at a glance, in a single score | 0–100 Business Health Scorecard (currently 75/100, "Healthy") |
| BR-02 | Identify customers likely to churn, ranked by revenue at stake | RFM-based churn segmentation + Win-Back Priority List |
| BR-03 | Quantify revenue recoverable through win-back action | ₹4,116K tied to at-risk/churned customers; 20% recovery ≈ ₹823K |
| BR-04 | Flag where discounting is destroying margin | Discount Elasticity Simulator + Leakage & Abuse module (299 orders, ₹34K margin impact) |
| BR-05 | Recommend a profit-maximizing discount level per sub-category | Profit-vs-discount elasticity curve, per sub-category |
| BR-06 | Surface which products/categories should be cross-sold together | Apriori market basket analysis, 52 rules (top: Baby Food → Diapers & Wipes, lift 9.58×) |
| BR-07 | Predict customer lifetime value to prioritize retention spend | Random Forest CLV model (R² = 0.930) |
| BR-08 | Segment customers by value and behavior | K-Means segmentation (silhouette = 0.611), 119 "Champion" customers identified |
| BR-09 | Explain retention patterns over time, not just a point-in-time snapshot | Cohort retention heatmap + Kaplan-Meier-style survival curve (median customer half-life ≈ 330 days) |
| BR-10 | Allow non-technical stakeholders to read findings without opening code | Auto-generated plain-English Executive Narrative on the Overview page |
| BR-11 | Allow technical/analyst users to ask custom questions of the data | Live SQL Analytics Lab (DuckDB), with preset queries (High-Value Customers, Loss-Making Sub-Categories, etc.) |

### 6. Non-Functional Requirements

- **Usability:** Must run with a single command (`run.bat` / `run.sh`) — no setup beyond `pip install`.
- **Portability:** Must accept a user-uploaded CSV and recompute every module against it, not just the bundled dataset.
- **Traceability:** Every headline number on the Overview page must be reproducible from the SQL layer.
- **Accessibility:** Atkinson Hyperlegible typeface used across the dashboard for readability.

### 7. Assumptions & Constraints

- Dataset is historical and static; forecasts (Holt-Winters, demand heatmap) are based on this snapshot and would need to be re-run periodically in a production setting.
- "Business Health Score" and thresholds (e.g. what counts as "at risk") are rule-based judgment calls, documented in-app, not externally benchmarked against the client's industry.
- No real stakeholder interviews were conducted (solo academic project); requirements above were derived from what a retail operations/marketing/pricing function would typically need, based on standard retail-analytics practice.

### 8. Success Metrics

| Metric | Target | Status |
|---|---|---|
| Business Health Score computed and explained in plain English | Yes | ✅ Delivered |
| At-risk revenue quantified in ₹ | Yes | ✅ ₹4,638K flagged at churn risk |
| At least one actionable, quantified recommendation per module | Yes | ✅ Each module ends in a ₹-value or ranked action list |
| Dashboard runnable by a non-technical user in under 5 minutes | Yes | ✅ One-click `run.bat`/`run.sh` |
