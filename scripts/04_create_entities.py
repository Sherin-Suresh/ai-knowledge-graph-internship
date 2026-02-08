import pandas as pd

df = pd.read_csv("data_staging/clean_tickets.csv")

# Customer entity
customers = df[['customer_id', 'Customer Email', 'Customer Gender', 'Customer Age']].drop_duplicates()
customers.to_csv("data_staging/customers.csv", index=False)

# Ticket entity
tickets = df[['Ticket ID', 'Ticket Subject', 'Ticket Status', 'Ticket Priority', 'Ticket Type']]
tickets.to_csv("data_staging/tickets.csv", index=False)

# Product entity
products = df[['product_id', 'Product Purchased']].drop_duplicates()
products.to_csv("data_staging/products.csv", index=False)

print("Entity tables created successfully.")
