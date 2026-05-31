import polars as pl
import json
import os

# Ensure the outputs folder exists
os.makedirs("outputs", exist_ok=True)

# Load the raw sales data
sales = pl.read_csv("data/raw/sales.csv")

# Identify bad rows (quantity 0 or less, missing price)
rows_loaded = sales.height
invalid_rows = sales.filter(
    (pl.col("quantity") <= 0) | 
    (pl.col("price").is_null())
)

report = {
    "rows_loaded": rows_loaded,
    "invalid_rows": invalid_rows.height,
    "rows_retained": rows_loaded - invalid_rows.height
}

# Save the report
with open("outputs/data_quality_report.json", "w") as f:
    json.dump(report, f, indent=4)

print("Data Quality Report generated:")
print(report)