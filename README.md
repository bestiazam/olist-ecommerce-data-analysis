# Olist E-Commerce Data Analysis

**End-to-end analytics portfolio project | SQL · Python · Excel (planned) · Power BI**

This project explores order activity, product sales, customer reviews, payments, and delivery performance using the public Brazilian E-Commerce Dataset by Olist.

## Business questions
- How many orders were placed, and how did activity change month by month?
- Which product categories generated the most product revenue?
- What payment methods were used?
- How were customer reviews distributed?
- What proportion of delivered orders arrived by the estimated delivery date?

## Key results
| Metric | Result |
| --- | ---: |
| Orders | 99,441 |
| Delivered orders | 96,478 |
| Share of orders marked delivered | 97.02% |
| Product revenue (item prices, excluding shipping) | R$ 13,591,643.70 |
| Freight charges | R$ 2,251,909.54 |
| Average item price | R$ 120.65 |

*These are historical dataset totals, not a current company financial report. Product revenue is the sum of order-item prices; it is not net profit or total payment receipts.*

## Repository layout
- `sql/olist_analysis.sql` — MySQL queries for orders, categories, reviews, payments and deliveries.
- `python/olist_analysis.py` — reproducible analysis script reading the original CSV files.
- `results/` — selected aggregate CSV outputs from the analysis.
- `images/` — charts from the analysis (to be added).
- `powerbi/` — Power BI report (to be added).
- `excel/` — Pivot Table analysis (planned).

## Run the Python analysis
Download the **Brazilian E-Commerce Public Dataset by Olist** from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), keeping the original CSV file names.

```bash
pip install -r requirements.txt
python python/olist_analysis.py --data-dir path/to/your/olist-files
```

Outputs are saved in `results/` and `images/`. The original raw datasets are not redistributed in this repository.

## Tools
MySQL · Python (pandas, matplotlib) · Power BI · Excel (planned)

## Notes and limitations
- Different tables have different grains (orders, order items, and payment installments). Their counts and sums should not be treated as interchangeable.
- `customer_id` identifies an order-associated customer record, while `customer_unique_id` is the better identifier for repeat-customer analysis.
- The SQL delivery analysis considers only delivered orders with actual and estimated delivery dates.
- The portfolio is being completed in stages; planned Excel and Power BI files will be added separately.

**Author:** Basti Azamzade
