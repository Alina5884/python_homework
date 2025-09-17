import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path("../db/lesson.db")

with sqlite3.connect(db_path) as conn:
    try:
        df = pd.read_sql_query("""
            SELECT li.line_item_id, li.quantity, p.product_id, p.product_name, p.price
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
        """, conn)
    except Exception:
        df = pd.read_sql_query("""
            SELECT od.order_detail_id AS line_item_id, od.quantity, p.product_id, p.product_name, p.price
            FROM order_details od
            JOIN products p ON od.product_id = p.product_id
        """, conn)

print(df.head())

df["total"] = df["quantity"] * df["price"]
print(df.head())

grouped = (
    df.groupby("product_id")
      .agg(line_item_count=("line_item_id","count"),
           total_revenue=("total","sum"),
           product_name=("product_name","first"))
      .reset_index()
      .sort_values("product_name")
)

print(grouped.head())

grouped.to_csv("order_summary.csv", index=False)
print("saved: order_summary.csv")