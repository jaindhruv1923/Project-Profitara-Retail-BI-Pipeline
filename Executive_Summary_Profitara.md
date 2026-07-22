# Executive Summary — Profitara
### Retail Intelligence Platform | India Quick-Commerce Dataset | 10,000 transactions

---

## Business Health: 75 / 100 — Healthy

Total revenue of **₹6.70M** at a **4.15% net margin** (₹278K net profit), which sits above the ~4% retail benchmark — the business is operationally efficient, but three specific leaks are costing it money right now.

---

## 1. Where money is leaking

- **Personal Care** is the highest-profit category. **Fresh Fruits** is the most loss-making sub-category — restructuring its discount policy could recover an estimated **₹38K**.
- **Discount abuse** affects 299 orders (3.0% of all orders) with discounts above 30%, destroying an estimated **₹34K in margin**.
- A discount-elasticity model shows several sub-categories are being discounted well past the point that maximizes profit — the simulator quantifies the exact optimal discount per sub-category.

**Recommendation:** Cap discounts on the flagged sub-categories at their profit-maximizing level; audit the 299 high-discount orders for policy violations.

---

## 2. Which customers are leaving, and what it's worth

- **South region** leads in revenue, but **1,003 customers** have been inactive for 90+ days — representing **₹4,638K** in potential lost annual revenue.
- Of the full customer base, 975 are already churned and 136 are actively "at risk," with **₹4,116K** in combined revenue tied to these two groups.
- A targeted win-back campaign recovering even 20% of this at-risk revenue would add **₹823K**.
- Customer survival analysis shows the median customer's "half-life" is approximately **330 days** — half of all customers stop purchasing within this window, meaning retention effort has the most leverage in the **first 165 days**.

**Recommendation:** Launch a win-back campaign prioritized by the ranked list of highest-revenue at-risk customers; concentrate retention spend on the first 165 days of the customer lifecycle.

---

## 3. What should be stocked and cross-sold

- Market basket analysis surfaced **52 cross-sell rules**. The strongest: **Baby Food + Diapers & Wipes** (lift 9.58×) — customers who buy one are far more likely to buy the other than chance would predict.
- 119 customers are identified as high-value "Champions" via behavioral segmentation, worth prioritizing for loyalty programs.
- A 12-month Customer Lifetime Value model (R² = 0.930) ranks customers by predicted future value, separate from past spend — useful for deciding who's worth retaining even if their recent activity looks flat.

**Recommendation:** Bundle Baby Food with Diapers & Wipes in promotions; build a loyalty tier around the 119 identified Champion customers.

---

## Bottom line

Profitara turns 10,000 raw transactions into three concrete, ₹-quantified actions: fix discounting on Fresh Fruits and the flagged sub-categories, run a win-back campaign targeting ₹4,116K in at-risk revenue, and bundle the top cross-sell pair. Each recommendation is traceable back to the underlying transaction data through the platform's SQL layer.
