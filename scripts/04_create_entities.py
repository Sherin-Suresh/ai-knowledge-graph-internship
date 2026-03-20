import pandas as pd
import os

STAGING_PATH = "data_staging"

customers_df = pd.read_csv(os.path.join(STAGING_PATH, "clean_customers.csv"))
products_df = pd.read_csv(os.path.join(STAGING_PATH, "clean_products.csv"))
orders_df = pd.read_csv(os.path.join(STAGING_PATH, "clean_orders.csv"))

# CUSTOMER ENTITY
customers = customers_df.drop_duplicates(subset=["customer_id"])
customers.to_csv(os.path.join(STAGING_PATH, "kg_customers.csv"), index=False)

# PRODUCT ENTITY
products = products_df.drop_duplicates(subset=["product_id"])
products.to_csv(os.path.join(STAGING_PATH, "kg_products.csv"), index=False)

# ORDER ENTITY
orders = orders_df.drop_duplicates(subset=["order_id"])
orders.to_csv(os.path.join(STAGING_PATH, "kg_orders.csv"), index=False)

print("Enterprise entity tables created successfully.")