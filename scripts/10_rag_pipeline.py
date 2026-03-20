"""
Milestone 3 — Part 2: Full RAG Pipeline
Includes:
  ✔ Real FAISS semantic search
  ✔ BM25 keyword search
  ✔ Hybrid Search (BM25 + FAISS)
  ✔ Neo4j Knowledge Graph query
  ✔ Ollama LLM (llama3)
  ✔ RAG chain — combines all context → LLM → final answer
"""

import pandas as pd
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_community.llms import Ollama
from neo4j import GraphDatabase

# ═══════════════════════════════════════════════════════════
# SECTION 1: Configuration — UPDATE THESE
# ═══════════════════════════════════════════════════════════

NEO4J_URI      = "bolt://localhost:7687"
NEO4J_USER     = "neo4j"
NEO4J_PASSWORD = "sHerin_1438"   # ← change this

OLLAMA_MODEL   = "tinyllama"               # make sure: ollama pull llama3

# ═══════════════════════════════════════════════════════════
# SECTION 2: Load Embedding Model
# ═══════════════════════════════════════════════════════════
print("\n--- Loading Embedding Model ---")
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
print("✅ Embedding model loaded.")

# ═══════════════════════════════════════════════════════════
# SECTION 3: Load FAISS Vector Database
# ═══════════════════════════════════════════════════════════
print("\n--- Loading FAISS Vector Database ---")
try:
    vector_db = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
    faiss_retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    print("✅ FAISS database loaded.")
except Exception as e:
    print(f"❌ Error loading FAISS index: {e}")
    print("Run 09_build_index.py first.")
    exit()

# ═══════════════════════════════════════════════════════════
# SECTION 4: Build BM25 Retriever
# ═══════════════════════════════════════════════════════════
print("\n--- Building BM25 Keyword Retriever ---")
try:
    customers = pd.read_csv("data_staging/clean_customers.csv").fillna("")
    products  = pd.read_csv("data_staging/clean_products.csv").fillna("")
    orders    = pd.read_csv("data_staging/clean_orders.csv").fillna(0)

    bm25_docs = []
    for row in customers.to_dict("records"):
        text = (f"Customer: {row['customer_name']} (ID: {row['customer_id']}) "
                f"from {row['region']}.")
        bm25_docs.append(Document(page_content=text,
            metadata={"source": "customers", "id": str(row["customer_id"])}))

    for row in products.to_dict("records"):
        text = (f"Product: {row['product_name']} | Category: {row['category']} "
                f"| Price: {row['unit_price']}")
        bm25_docs.append(Document(page_content=text,
            metadata={"source": "products", "id": str(row["product_id"])}))

    for row in orders.head(1000).to_dict("records"):
        text = (f"Order: {row['order_id']} | Customer {row['customer_id']} "
                f"bought product {row['product_id']}")
        bm25_docs.append(Document(page_content=text,
            metadata={"source": "orders", "id": str(row["order_id"])}))

    bm25_retriever = BM25Retriever.from_documents(bm25_docs)
    bm25_retriever.k = 3
    print("✅ BM25 retriever ready.")
except Exception as e:
    print(f"❌ Error building BM25 retriever: {e}")
    exit()

# ═══════════════════════════════════════════════════════════
# SECTION 5: Hybrid Retriever (BM25 + FAISS)
# ═══════════════════════════════════════════════════════════
print("\n--- Setting Up Hybrid Retriever ---")
# REPLACE WITH THIS
def hybrid_retrieve(query, k=3):
    bm25_results = bm25_retriever.invoke(query)
    faiss_results = faiss_retriever.invoke(query)
    seen = set()
    combined = []
    for doc in bm25_results + faiss_results:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            combined.append(doc)
    return combined[:k*2]

print("✅ Hybrid retriever ready (BM25 + FAISS).")

# ═══════════════════════════════════════════════════════════
# SECTION 6: Neo4j Knowledge Graph
# ═══════════════════════════════════════════════════════════
print("\n--- Connecting to Neo4j ---")
try:
    neo4j_driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
    )
    neo4j_driver.verify_connectivity()
    print("✅ Neo4j connected.")
except Exception as e:
    print(f"⚠️  Neo4j connection failed: {e}")
    print("Neo4j context will be skipped. RAG pipeline will still work.")
    neo4j_driver = None


def query_neo4j(cypher_query: str) -> str:
    if neo4j_driver is None:
        return "Neo4j not available."
    try:
        with neo4j_driver.session() as session:
            result = session.run(cypher_query)
            rows = [str(dict(record)) for record in result]
            if not rows:
                return "No results found in graph."
            return "\n".join(rows[:10])
    except Exception as e:
        return f"Graph query error: {e}"


def get_graph_context(user_query: str) -> str:
    q = user_query.lower()
    if "north" in q or "region" in q:
        cypher = """
            MATCH (c:Customer)
            WHERE c.region = 'North'
            RETURN c.customer_name AS name, c.customer_id AS id
            LIMIT 10
        """
    elif "apparel" in q or "category" in q:
        cypher = """
            MATCH (p:Product)
            WHERE p.category = 'Apparel'
            RETURN p.product_name AS name, p.unit_price AS price
            LIMIT 10
        """
    elif "order" in q or "bought" in q or "purchased" in q:
        cypher = """
            MATCH (c:Customer)-[:PLACED]->(o:Order)-[:CONTAINS]->(p:Product)
            RETURN c.customer_name AS customer, p.product_name AS product,
                   o.order_id AS order
            LIMIT 10
        """
    elif "product" in q:
        cypher = """
            MATCH (p:Product)
            RETURN p.product_name AS name, p.category AS category,
                   p.unit_price AS price
            LIMIT 10
        """
    else:
        cypher = """
            MATCH (c:Customer)-[:PLACED]->(o:Order)
            RETURN c.customer_name AS customer, count(o) AS total_orders
            ORDER BY total_orders DESC
            LIMIT 10
        """
    return query_neo4j(cypher)

# ═══════════════════════════════════════════════════════════
# SECTION 7: Ollama LLM
# ═══════════════════════════════════════════════════════════
print("\n--- Loading Ollama LLM ---")
try:
    llm = Ollama(model=OLLAMA_MODEL)
    print(f"✅ Ollama loaded with model: {OLLAMA_MODEL}")
except Exception as e:
    print(f"❌ Error loading Ollama: {e}")
    print("Make sure Ollama is running: ollama serve")
    print("And model is pulled: ollama pull llama3")
    exit()

# ═══════════════════════════════════════════════════════════
# SECTION 8: RAG Prompt
# ═══════════════════════════════════════════════════════════
RAG_PROMPT_TEMPLATE = """
You are an intelligent data assistant for a retail business.
You have access to two sources of context below.

--- VECTOR SEARCH CONTEXT (from FAISS) ---
{context}

--- KNOWLEDGE GRAPH CONTEXT (from Neo4j) ---
{graph_context}

Use BOTH sources of context to answer the question accurately and concisely.
If you cannot find the answer in either source, say:
"I don't have enough data to answer this."

Question: {question}

Answer:
"""

rag_prompt = PromptTemplate(
    input_variables=["context", "graph_context", "question"],
    template=RAG_PROMPT_TEMPLATE
)

# ═══════════════════════════════════════════════════════════
# SECTION 9: Main GraphRAG Query Function
# ═══════════════════════════════════════════════════════════

def ask(user_query: str):
    print(f"\n{'═'*60}")
    print(f"🔍 Query: {user_query}")
    print(f"{'═'*60}")

    # Step 1: Hybrid search
    print("  [1/3] Running hybrid search...")
    retrieved_docs = hybrid_retrieve(user_query)
    vector_context = "\n".join([doc.page_content for doc in retrieved_docs])

    # Step 2: Neo4j graph context
    print("  [2/3] Querying knowledge graph...")
    graph_context = get_graph_context(user_query)

    # Step 3: LLM answer
    print("  [3/3] Generating answer with LLM...")
    filled_prompt = rag_prompt.format(
        context=vector_context,
        graph_context=graph_context,
        question=user_query
    )
    answer = llm.invoke(filled_prompt)

    print(f"\n💬 Answer:\n{answer}")
    print(f"{'─'*60}")
    return answer


# ═══════════════════════════════════════════════════════════
# SECTION 10: Test Queries + Interactive Mode
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("\n\n🚀 Running Test Queries...\n")

    ask("Find customers from the North region")
    ask("Which products are in the Apparel category?")
    ask("Show me orders for product 1005")
    ask("Which customers purchased the most products?")

    print("\n\n✅ All test queries done.")
    print("─" * 60)
    print("Entering interactive mode. Type 'exit' to quit.\n")

    while True:
        user_input = input("Ask a question: ").strip()
        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        if user_input:
            ask(user_input)