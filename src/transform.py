import polars as pl
import os

print("Starting transformation process...")

# Ensure processed folder exists
os.makedirs("data/processed", exist_ok=True)

# 1. Load Raw Data
sales = pl.read_csv("data/raw/sales.csv")
products = pl.read_csv("data/raw/products.csv")
stores = pl.read_csv("data/raw/stores.csv")

initial_sales_count = sales.height

# 2. Clean Sales Data (Filter out invalid rows)
clean_sales = sales.filter(
    (pl.col("quantity") > 0) & 
    (pl.col("price").is_not_null())
)

# Convert strings to Datetime (strict=False turns "bad_timestamp" into a null value)
clean_sales = clean_sales.with_columns(
    pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S.%f", strict=False)
)

# Drop the row where timestamp became null
clean_sales = clean_sales.filter(pl.col("timestamp").is_not_null())

# Add total_sale column
clean_sales = clean_sales.with_columns(
    (pl.col("quantity") * pl.col("price")).alias("total_sale")
)

# 3. Standardize Text Fields
clean_products = products.with_columns(
    pl.col("product_name").str.strip_chars().str.to_titlecase(),
    pl.col("category").str.strip_chars().str.to_uppercase()
)

clean_stores = stores.with_columns(
    pl.col("store_name").str.strip_chars().str.to_titlecase(),
    pl.col("city").str.strip_chars().str.to_uppercase()
)

# 4. Save to Processed Directory
clean_sales.write_csv("data/processed/cleaned_sales.csv")
clean_products.write_csv("data/processed/cleaned_products.csv")
clean_stores.write_csv("data/processed/cleaned_stores.csv")

# 5. Output Results
print(f"Transformation complete.")
print(f"Initial rows: {initial_sales_count}")
print(f"Clean rows: {clean_sales.height}")
print(f"Dropped invalid rows: {initial_sales_count - clean_sales.height}")