import pandas as pd
import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DeterministicFakeEmbedding

# 1. Load datasets from data_staging/
print("--- Loading Datasets from data_staging/ ---")
try:
    # Matching your exact file names in the image
    customers = pd.read_csv("data_staging/clean_customers.csv").fillna("")
    products = pd.read_csv("data_staging/clean_products.csv").fillna("")
    orders = pd.read_csv("data_staging/clean_orders.csv").fillna(0)
    print(f"✅ Loaded {len(customers)} customers, {len(products)} products, and {len(orders)} orders.")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Double check that you are running this from the main project folder.")
    exit()

documents = []

# 2. Process Customers
for row in customers.to_dict('records'):
    text = f"Customer: {row['customer_name']} (ID: {row['customer_id']}) from {row['region']}."
    documents.append(Document(page_content=text, metadata={"source": "customers", "id": str(row['customer_id'])}))

# 3. Process Products
for row in products.to_dict('records'):
    text = f"Product: {row['product_name']} | Category: {row['category']} | Price: {row['unit_price']}"
    documents.append(Document(page_content=text, metadata={"source": "products", "id": str(row['product_id'])}))

# 4. Process Orders
# Using head(1000) to ensure a fast, successful run
for row in orders.head(1000).to_dict('records'):
    text = f"Order: {row['order_id']} | Customer {row['customer_id']} bought product {row['product_id']}"
    documents.append(Document(page_content=text, metadata={"source": "orders", "id": str(row['order_id'])}))

# 5. Initialize Safe Embedding Model
print("--- Initializing Safe Embedding Model ---")
embedding_model = DeterministicFakeEmbedding(size=384)

# 6. Build and Save FAISS Index
print(f"--- Building FAISS Index with {len(documents)} documents ---")
try:
    # FAISS is the most stable choice for your Windows setup
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local("faiss_index")
    
    print(f"\n✅ SUCCESS: Milestone 3 Part 1 Complete!")
    print(f"Vector database folder 'faiss_index' created successfully.")

except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")