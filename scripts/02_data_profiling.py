import pandas as pd

customers = pd.read_csv("data_raw/dim_customer.csv")
products = pd.read_csv("data_raw/dim_product.csv")
orders = pd.read_csv("data_raw/fact_order.csv")

print("Customers Missing:\n", customers.isnull().sum())
print("Products Missing:\n", products.isnull().sum())
print("Orders Missing:\n", orders.isnull().sum())

print("Duplicate Customers:", customers.duplicated().sum())
print("Duplicate Products:", products.duplicated().sum())
print("Duplicate Orders:", orders.duplicated().sum())