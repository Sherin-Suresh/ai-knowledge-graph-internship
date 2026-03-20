import pandas as pd
import spacy

# Load your existing data
customers = pd.read_csv("data_staging/clean_customers.csv")
products = pd.read_csv("data_staging/clean_products.csv")
orders = pd.read_csv("data_staging/clean_orders.csv")

# Generate natural sentences from real data
sentences = []

for i in range(10):   # take first 10 rows
    customer = customers.iloc[i]["customer_name"]
    product = products.iloc[i]["product_name"]
    order = orders.iloc[i]["order_id"]

    sentence = f"{customer} placed order {order} for {product}."
    sentences.append(sentence)

text_data = " ".join(sentences)

print("Generated Text:")
print(text_data)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

doc = nlp(text_data)

# 🔥 Extract entities properly
customers_extracted = []
products_extracted = []

for ent in doc.ents:
    print(ent.text, ent.label_)   # optional: to see what is detected

    if ent.label_ == "PERSON":
        customers_extracted.append(ent.text)

    if ent.label_ in ["PRODUCT", "ORG"]:
        products_extracted.append(ent.text)

# Save extracted entities
pd.DataFrame(list(set(customers_extracted)), columns=["name"]).to_csv(
    "data_staging/llm_customers.csv", index=False
)

pd.DataFrame(list(set(products_extracted)), columns=["name"]).to_csv(
    "data_staging/llm_products.csv", index=False
)

print("LLM-based NER completed.")