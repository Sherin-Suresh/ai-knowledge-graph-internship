from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DeterministicFakeEmbedding

# 1. Setup the same "Safe" model we used to build the index
print("--- Loading Search Engine ---")
embedding_model = DeterministicFakeEmbedding(size=384)

# 2. Load the FAISS database you just found
try:
    vector_db = FAISS.load_local(
        "faiss_index", 
        embedding_model, 
        allow_dangerous_deserialization=True
    )
    print("✅ Vector Database loaded successfully.")
except Exception as e:
    print(f"❌ Error loading index: {e}")
    exit()

# 3. Define a search function
def search_my_data(query):
    print(f"\n🔍 Searching for: '{query}'")
    # This finds the 3 most similar results based on MEANING, not just keywords
    results = vector_db.similarity_search(query, k=3)
    
    print("-" * 50)
    for i, doc in enumerate(results):
        print(f"Result {i+1}: {doc.page_content}")
    print("-" * 50)

# 4. Test Queries
search_my_data("Find customers from the North region")
search_my_data("Which products are in the Apparel category?")
search_my_data("Check orders for product 1005")