"""Olist e-commerce analysis using raw CSV files from the public Olist dataset.

Usage:
    pip install -r requirements.txt
    python python/olist_analysis.py --data-dir path/to/olist-csv-folder

Output files are written to results/ and images/ by default.
"""
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True, help="Folder containing original Olist CSV files")
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    parser.add_argument("--images-dir", type=Path, default=Path("images"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.images_dir.mkdir(parents=True, exist_ok=True)
    def load(name):
        return pd.read_csv(args.data_dir / name)
    orders = load("olist_orders_dataset.csv")
    items = load("olist_order_items_dataset.csv")
    products = load("olist_products_dataset.csv")
    orders.isna().sum().rename("missing_count").to_csv(args.output_dir / "missing_values.csv")
    orders.order_status.value_counts().rename("count").to_csv(args.output_dir / "order_status_counts.csv")
    orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"], errors="coerce")
    dated = orders.dropna(subset=["order_purchase_timestamp"]).copy()
    dated["month"] = dated.order_purchase_timestamp.dt.to_period("M").astype(str)
    monthly_orders = dated.groupby("month").order_id.nunique().sort_index()
    monthly_orders.rename("orders").to_csv(args.output_dir / "monthly_orders.csv")
    merged = items.merge(products[["product_id", "product_category_name"]], on="product_id", how="left", validate="many_to_one")
    merged["product_category_name"] = merged["product_category_name"].fillna("Uncategorized")
    # Large joined data is intentionally not exported to the public repository.
    cat_revenue = merged.groupby("product_category_name").price.sum().sort_values(ascending=False)
    cat_revenue.rename("product_revenue_brl").to_csv(args.output_dir / "category_revenue.csv")
    item_dates = items.merge(dated[["order_id","month"]], on="order_id", how="inner", validate="many_to_one")
    monthly_revenue = item_dates.groupby("month").price.sum().sort_index()
    monthly_revenue.rename("product_revenue_brl").to_csv(args.output_dir / "monthly_revenue.csv")
    kpis = pd.DataFrame({
        "KPI": ["Total Orders", "Delivered Orders", "Delivered Percentage",
                "Total Product Revenue", "Total Freight Value", "Product Revenue Plus Freight",
                "Average Product Revenue Per Order"],
        "Value": [orders.order_id.nunique(), orders.order_status.eq("delivered").sum(),
                  round(100 * orders.order_status.eq("delivered").mean(), 2),
                  round(items.price.sum(), 2), round(items.freight_value.sum(), 2),
                  round((items.price + items.freight_value).sum(), 2),
                  round(items.price.sum() / orders.order_id.nunique(), 2)]
    })
    kpis.to_csv(args.output_dir / "olist_kpis.csv", index=False)
    def line_plot(series, title, ylabel, filename):
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(series.index, series.values, marker="o")
        ax.set(title=title, xlabel="Month", ylabel=ylabel)
        ax.tick_params(axis="x", labelrotation=65)
        fig.tight_layout()
        fig.savefig(args.images_dir / filename, dpi=200)
        plt.close(fig)
    line_plot(monthly_orders, "Monthly Number of Orders", "Orders", "monthly_orders.png")
    line_plot(monthly_revenue, "Monthly Product Revenue", "BRL", "monthly_revenue.png")
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_revenue.head(10).sort_values().plot.barh(ax=ax)
    ax.set(title="Top 10 Product Categories by Revenue", xlabel="Product Revenue (BRL)", ylabel="Category")
    fig.tight_layout()
    fig.savefig(args.images_dir / "top_categories_revenue.png", dpi=200)
    plt.close(fig)
    print(kpis.to_string(index=False))

if __name__ == "__main__":
    main()
