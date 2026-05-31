import duckdb
import os

print("Starting database load process...")

# Ensure outputs folder exists for the database file
os.makedirs("outputs", exist_ok=True)
db_path = "outputs/warehouse.db"

# Connect to DuckDB
con = duckdb.connect(db_path)

# 1. Execute the DDL schema (FOOLPROOF EMBEDDED METHOD)
print("Creating tables directly...")

schema_sql = """
CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR,
    category VARCHAR
);

CREATE TABLE IF NOT EXISTS dim_store (
    store_id INTEGER PRIMARY KEY,
    store_name VARCHAR,
    city VARCHAR
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key DATE PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    day_of_week INTEGER
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER,
    store_id INTEGER,
    date_key DATE,
    quantity INTEGER,
    price DOUBLE,
    total_sale DOUBLE,
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);
"""

# Execute the entire block at once
con.execute(schema_sql)
print("Tables created successfully. Loading data...")

# 2. Load Dimensions from processed CSVs
con.execute("""
    INSERT INTO dim_product 
    SELECT * FROM read_csv_auto('data/processed/cleaned_products.csv')
    ON CONFLICT DO NOTHING;
""")

con.execute("""
    INSERT INTO dim_store 
    SELECT * FROM read_csv_auto('data/processed/cleaned_stores.csv')
    ON CONFLICT DO NOTHING;
""")

# 3. Build Date Dimension & Load Fact Table
print("Loading facts and generating date dimension...")

con.execute("""
    INSERT INTO dim_date 
    SELECT DISTINCT 
        CAST(timestamp AS DATE) AS date_key,
        EXTRACT(YEAR FROM timestamp) AS year,
        EXTRACT(MONTH FROM timestamp) AS month,
        EXTRACT(DAY FROM timestamp) AS day,
        EXTRACT(ISODOW FROM timestamp) AS day_of_week
    FROM read_csv_auto('data/processed/cleaned_sales.csv')
    ON CONFLICT DO NOTHING;
""")

con.execute("""
    INSERT INTO fact_sales 
    SELECT 
        sale_id,
        product_id,
        store_id,
        CAST(timestamp AS DATE) AS date_key,
        quantity,
        price,
        total_sale
    FROM read_csv_auto('data/processed/cleaned_sales.csv')
    ON CONFLICT DO NOTHING;
""")

# Verify the load
tables = ["dim_product", "dim_store", "dim_date", "fact_sales"]
print("\n--- Database Load Summary ---")
for table in tables:
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")

con.close()
print("\nWarehouse loaded successfully at outputs/warehouse.db")