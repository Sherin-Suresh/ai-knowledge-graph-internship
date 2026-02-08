import pandas as pd

# Load raw data
df = pd.read_csv("data_raw/customer_support_tickets.csv")

# 1. Remove duplicate rows
df = df.drop_duplicates()

# 2. Handle missing values
df['Ticket Priority'] = df['Ticket Priority'].fillna('Medium')
df['Ticket Status'] = df['Ticket Status'].fillna('open')
df['Resolution'] = df['Resolution'].fillna('Not Provided')

# 3. Standardize text columns
df['Ticket Priority'] = df['Ticket Priority'].str.capitalize()
df['Ticket Status'] = df['Ticket Status'].str.lower()
df['Ticket Type'] = df['Ticket Type'].str.lower()

# 4. Convert date columns
df['Date of Purchase'] = pd.to_datetime(df['Date of Purchase'], errors='coerce')

# 5. Create IDs for KG
df['customer_id'] = df['Customer Email'].factorize()[0]
df['product_id'] = df['Product Purchased'].factorize()[0]

# Save cleaned dataset
df.to_csv("data_staging/clean_tickets.csv", index=False)

print("Preprocessing completed. Clean data saved to data_staging/")
