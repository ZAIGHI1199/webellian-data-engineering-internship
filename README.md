# Webellian Data Engineering Pipeline

A robust, end-to-end local data pipeline demonstrating automated ingestion, strict data quality validation, modern transformations, and dimensional modeling. 

Built with **Python**, **Polars**, and **DuckDB**.

## Architecture Overview

This project simulates a production-grade ETL/ELT workflow:
1. **Generation:** Programmatically creates realistic sales, product, and store datasets using `Faker`.
2. **Validation:** Identifies and logs missing values and invalid constraints before processing.
3. **Transformation:** Uses **Polars** to rapidly clean data, handle bad types, standardise text, and calculate derived metrics (`total_sale`).
4. **Data Modeling:** Uses **DuckDB** to build a robust Star Schema (`fact_sales`, `dim_product`, `dim_store`, `dim_date`) from the cleaned data.
5. **Analytics:** Executes SQL queries directly against the warehouse to generate business insights.

## Tech Stack Choices
* **Polars:** Chosen over standard Pandas for its exceptional performance, strict typing, and multi-threaded execution, demonstrating familiarity with modern, scalable data processing frameworks.
* **DuckDB:** An incredibly fast, in-process analytical database. It allows for rigorous SQL data modeling (DDL) and querying without requiring the reviewer to set up external database infrastructure.
* **Pandera / Custom Validation:** Prioritises data quality by explicitly catching bad rows rather than allowing silent failures.

##  Project Structure
webellian-data-pipeline/
├── data/
│   ├── raw/                 # Generated source CSVs
│   └── processed/           # Cleaned, standardized CSVs ready for DB load
├── outputs/                 # Data quality reports, DB file, and final insight CSVs
├── src/
│   ├── generate_data.py     # Data generation script
│   ├── validate.py          # Validation layer
│   ├── transform.py         # Polars transformation logic
│   ├── load.py              # DuckDB DDL and data loading
│   └── analytics.py         # SQL insight generation
├── requirements.txt         # Dependencies
└── README.md