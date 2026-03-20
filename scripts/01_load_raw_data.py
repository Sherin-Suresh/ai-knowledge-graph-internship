import pandas as pd

customers = pd.read_csv("data_raw/dim_customer.csv")
products = pd.read_csv("data_raw/dim_product.csv")
orders = pd.read_csv("data_raw/fact_order.csv")

print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)