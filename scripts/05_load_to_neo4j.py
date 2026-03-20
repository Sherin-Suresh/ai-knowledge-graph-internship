from neo4j import GraphDatabase
import pandas as pd
import os

# ----------------------------
# Neo4j Connection
# ----------------------------
URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "sHerin_1438"

driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

STAGING_PATH = "data_staging"

# ----------------------------
# Load CSV Files
# ----------------------------
customers = pd.read_csv(os.path.join(STAGING_PATH, "kg_customers.csv"))
products = pd.read_csv(os.path.join(STAGING_PATH, "kg_products.csv"))
orders = pd.read_csv(os.path.join(STAGING_PATH, "clean_orders.csv"))

# LLM extracted entities
llm_customers = pd.read_csv(os.path.join(STAGING_PATH, "llm_customers.csv"))
llm_products = pd.read_csv(os.path.join(STAGING_PATH, "llm_products.csv"))


# ----------------------------
# Clear Graph
# ----------------------------
def clear_graph(tx):
    tx.run("MATCH (n) DETACH DELETE n")


# ----------------------------
# Load Data into Neo4j
# ----------------------------
def load_data(tx):

    # ----------------------------
    # Create Customers
    # ----------------------------
    for _, row in customers.iterrows():
        tx.run("""
            MERGE (c:Customer {customer_id: $id})
            SET c += $props
        """, id=row["customer_id"], props=row.to_dict())

    # ----------------------------
    # Create Products
    # ----------------------------
    for _, row in products.iterrows():
        tx.run("""
            MERGE (p:Product {product_id: $id})
            SET p += $props
        """, id=row["product_id"], props=row.to_dict())

    # ----------------------------
    # Create Orders + Relationships
    # ----------------------------
    for _, row in orders.iterrows():
        tx.run("""
            MERGE (o:Order {order_id: $order_id})
            SET o += $props

            WITH o
            MATCH (c:Customer {customer_id: $customer_id})
            MERGE (c)-[:PLACED]->(o)

            WITH o
            MATCH (p:Product {product_id: $product_id})
            MERGE (o)-[:CONTAINS]->(p)

            WITH o
            MATCH (c:Customer {customer_id: $customer_id})
            MATCH (p:Product {product_id: $product_id})
            MERGE (c)-[:PURCHASED]->(p)
        """,
        order_id=row["order_id"],
        customer_id=row["customer_id"],
        product_id=row["product_id"],
        props=row.to_dict()
        )

    # ----------------------------
    # Integrate LLM Extracted Customers
    # (Enhancement Layer)
    # ----------------------------
    for _, row in llm_customers.iterrows():
        tx.run("""
            MERGE (c:Customer {name: $name})
            SET c.llm_extracted = true
        """, name=row["name"])

    # ----------------------------
    # Integrate LLM Extracted Products
    # ----------------------------
    for _, row in llm_products.iterrows():
        tx.run("""
            MERGE (p:Product {name: $name})
            SET p.llm_extracted = true
        """, name=row["name"])


# ----------------------------
# Execute
# ----------------------------
with driver.session() as session:
    session.execute_write(clear_graph)
    session.execute_write(load_data)

driver.close()

print("Knowledge Graph Built Successfully with LLM Enhancement.")