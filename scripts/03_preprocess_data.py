import pandas as pd

customers = pd.read_csv("data_raw/dim_customer.csv")
products = pd.read_csv("data_raw/dim_product.csv")
orders = pd.read_csv("data_raw/fact_order.csv")

# Basic cleaning
customers = customers.drop_duplicates()
products = products.drop_duplicates()
orders = orders.drop_duplicates()

orders = orders.dropna()

# Save clean data
customers.to_csv("data_staging/clean_customers.csv", index=False)
products.to_csv("data_staging/clean_products.csv", index=False)
orders.to_csv("data_staging/clean_orders.csv", index=False)

print("Staging data created successfully.")