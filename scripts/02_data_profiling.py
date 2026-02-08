import pandas as pd

df = pd.read_csv("data_raw/customer_support_tickets.csv")

print("Missing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nUnique values per column:")
print(df.nunique())
