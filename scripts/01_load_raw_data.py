import pandas as pd

# Load raw dataset
file_path = "data_raw/customer_support_tickets.csv"
df = pd.read_csv(file_path)

# Show first 5 rows
print("First 5 rows of raw data:")
print(df.head())

# Show dataset structure
print("\nDataset Info:")
print(df.info())

# Show column names
print("\nColumn Names:")
print(df.columns)
