# Profitara: Retail BI Dimensional Modeling & DAX Catalog

## 1. Schema Layout
- Fact Table: `fact_sales` (10,000+ Indian quick-commerce transactions)
- Dimension Tables: `dim_customer`, `dim_product`, `dim_store`, `dim_date`

## 2. Core VertiPaq DAX Calculations
- CLV Rolling 90-Day Active Window
- Basket Affinity Repurchase Metric
- Churn Risk Classification Probability

## 3. Query Optimization
Partitioned along quarterly fiscal boundaries for sub-second visual refresh in Power BI.