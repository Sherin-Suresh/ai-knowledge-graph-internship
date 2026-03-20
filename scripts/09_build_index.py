"""
Milestone 3 — Part 1: Build FAISS Vector Index
Replace fake embeddings with real sentence-transformers embeddings.
Run this ONCE to rebuild your faiss_index folder.
"""

import pandas as pd
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ─────────────────────────────────────────────
# 1. Load Datasets
# ─────────────────────────────────────────────
print("\n--- Loading Datasets from data_staging/ ---")
try:
    customers = pd.read_csv("data_staging/clean_customers.csv").fillna("")
    products  = pd.read_csv("data_staging/clean_products.csv").fillna("")
    orders    = pd.read_csv("data_staging/clean_orders.csv").fillna(0)
    print(f"✅ Loaded {len(customers)} customers, {len(products)} products, {len(orders)} orders.")
except Exception as e:
    print(f"❌ Error loading data: {e}")
    print("Make sure you are running this from the main project folder.")
    exit()

# ─────────────────────────────────────────────
# 2. Convert Rows → LangChain Documents
# ─────────────────────────────────────────────
documents = []

for row in customers.to_dict("records"):
    text = (
        f"Customer: {row['customer_name']} (ID: {row['customer_id']}) "
        f"from {row['region']}."
    )
    documents.append(Document(
        page_content=text,
        metadata={"source": "customers", "id": str(row["customer_id"])}
    ))

for row in products.to_dict("records"):
    text = (
        f"Product: {row['product_name']} | Category: {row['category']} "
        f"| Price: {row['unit_price']}"
    )
    documents.append(Document(
        page_content=text,
        metadata={"source": "products", "id": str(row["product_id"])}
    ))

for row in orders.head(1000).to_dict("records"):
    text = (
        f"Order: {row['order_id']} | Customer {row['customer_id']} "
        f"bought product {row['product_id']}"
    )
    documents.append(Document(
        page_content=text,
        metadata={"source": "orders", "id": str(row["order_id"])}
    ))

print(f"✅ Converted {len(documents)} rows into documents.")

# ─────────────────────────────────────────────
# 3. Real Embedding Model (sentence-transformers)
# First run will auto-download the model (~90 MB).
# ─────────────────────────────────────────────
print("\n--- Loading Real Embedding Model ---")
print("(First run will download ~90 MB — this is normal)")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("✅ Embedding model ready.")

# ─────────────────────────────────────────────
# 4. Build & Save FAISS Index
# ─────────────────────────────────────────────
print(f"\n--- Building FAISS Index with {len(documents)} documents ---")
try:
    vectorstore = FAISS.from_documents(documents, embedding_model)
    vectorstore.save_local("faiss_index")
    print("\n✅ SUCCESS: FAISS index saved to 'faiss_index/' folder.")
    print("Now run: python milestone3_rag_pipeline.py")
except Exception as e:
    print(f"❌ Error building index: {e}")