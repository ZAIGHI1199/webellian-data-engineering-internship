from faker import Faker
import polars as pl
import random
from datetime import datetime, timedelta

fake = Faker()

categories = [
    "Electronics",
    "Books",
    "Sports",
    "Home"
]

products = []

for i in range(1, 31):
    products.append({
        "product_id": i,
        "product_name": fake.word().title(),
        "category": random.choice(categories)
    })

stores = [
    {"store_id": 1, "store_name": "Central Store", "city": "Rome"},
    {"store_id": 2, "store_name": "North Store", "city": "Milan"},
    {"store_id": 3, "store_name": "South Store", "city": "Naples"},
    {"store_id": 4, "store_name": "West Store", "city": "Turin"},
    {"store_id": 5, "store_name": "East Store", "city": "Florence"}
]

sales = []

start = datetime.now() - timedelta(days=90)

for i in range(1, 1501):

    ts = start + timedelta(
        days=random.randint(0, 90),
        hours=random.randint(0, 23)
    )

    sales.append({
        "sale_id": i,
        "product_id": random.randint(1, 30),
        "store_id": random.randint(1, 5),
        "quantity": random.randint(1, 10),
        "price": round(random.uniform(10, 500), 2),
        "timestamp": ts.isoformat()
    })

sales[10]["quantity"] = -5
sales[20]["price"] = None
sales[30]["timestamp"] = "bad_timestamp"

pl.DataFrame(products).write_csv("data/raw/products.csv")
pl.DataFrame(stores).write_csv("data/raw/stores.csv")
pl.DataFrame(sales).write_csv("data/raw/sales.csv")

print("Data generated")