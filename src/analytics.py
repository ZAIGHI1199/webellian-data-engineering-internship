import duckdb
import pandas as pd
import os

print("Generating business insights...")

# Connect to the loaded warehouse
db_path = "outputs/warehouse.db"
if not os.path.exists(db_path):
    print("Error: Database not found. Did you run load.py?")
    exit(1)

con = duckdb.connect(db_path)

# Insight 1: Revenue by City
print("\n--- Insight 1: Total Revenue by City ---")
query_city_revenue = """
    SELECT 
        ds.city,
        SUM(fs.total_sale) AS total_revenue,
        COUNT(fs.sale_id) AS total_transactions
    FROM fact_sales fs
    JOIN dim_store ds ON fs.store_id = ds.store_id
    GROUP BY ds.city
    ORDER BY total_revenue DESC;
"""
city_revenue_df = con.execute(query_city_revenue).fetchdf()
print(city_revenue_df.to_string(index=False))
city_revenue_df.to_csv("outputs/insight_revenue_by_city.csv", index=False)


# Insight 2: Top 5 Products by Revenue
print("\n--- Insight 2: Top 5 Products by Revenue ---")
query_top_products = """
    SELECT 
        dp.product_name,
        dp.category,
        SUM(fs.total_sale) AS total_revenue,
        SUM(fs.quantity) AS total_units_sold
    FROM fact_sales fs
    JOIN dim_product dp ON fs.product_id = dp.product_id
    GROUP BY dp.product_name, dp.category
    ORDER BY total_revenue DESC
    LIMIT 5;
"""
top_products_df = con.execute(query_top_products).fetchdf()
print(top_products_df.to_string(index=False))
top_products_df.to_csv("outputs/insight_top_products.csv", index=False)

con.close()
print("\nInsights saved to outputs/ directory.")