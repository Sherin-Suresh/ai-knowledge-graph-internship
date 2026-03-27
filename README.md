# 🚀 Enterprise Knowledge Graph Project

## 📌 Project Overview

This project builds a complete **Enterprise Knowledge Graph System** from raw customer data to an intelligent, queryable system.

### 🔹 Features

* Data ingestion and preprocessing
* Entity creation & LLM-based Named Entity Recognition (NER)
* Knowledge Graph construction using Neo4j
* Semantic search (FAISS + BM25)
* RAG (Retrieval-Augmented Generation) pipeline
* Interactive dashboard UI

---

## ⚙️ System Workflow

```
Raw Data (data_raw/*.csv)

↓
01_load_raw_data.py
→ 02_data_profiling.py
→ 03_preprocess_data.py

↓
04_create_entities.py
→ Create Entity CSVs (kg_*.csv)

↓
05_load_to_neo4j.py

↓
06_apply_llm_ner.py

↓
07_create_embeddings.py

↓
08_test_search.py

↓
09_build_index.py

↓
10_rag_pipeline.py

↓
API / Frontend Dashboard
```

---

## 📂 Repository Structure

```
ai-knowledge-graph-internship/
│
├── .vscode/               
├── data_raw/              
│   ├── dim_customer.csv
│   ├── dim_product.csv
│   └── fact_order.csv
│
├── data_staging/          
│   ├── clean_customers.csv    
│   ├── clean_products.csv     
│   ├── clean_orders.csv       
│   ├── kg_customers.csv       
│   ├── kg_products.csv        
│   ├── kg_orders.csv          
│   ├── llm_customers.csv      
│   └── llm_products.csv       
│
├── scripts/               
│   ├── 01_load_raw_data.py
│   ├── 02_data_profiling.py
│   ├── 03_preprocess_data.py
│   ├── 04_create_entities.py
│   ├── 05_load_to_neo4j.py
│   ├── 06_apply_llm_ner.py
│   ├── 07_create_embeddings.py
│   ├── 08_test_search.py
│   ├── 09_build_index.py
│   └── 10_rag_pipeline.py
│
├── momndaughtereatsdp.jpeg
├── README.md
├── requirements.txt
├── license.txt
└── .gitignore
```

---

## ▶️ How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Sherin-Suresh/ai-knowledge-graph-internship.git
cd ai-knowledge-graph-internship
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Scripts

#### Step 1: Data Processing

```bash
python scripts/01_load_raw_data.py
python scripts/02_data_profiling.py
python scripts/03_preprocess_data.py
```

#### Step 2: Knowledge Graph

```bash
python scripts/04_create_entities.py
python scripts/05_load_to_neo4j.py
```

#### Step 3: NER & Embeddings

```bash
python scripts/06_apply_llm_ner.py
python scripts/07_create_embeddings.py
```

#### Step 4: Search

```bash
python scripts/08_test_search.py
python scripts/09_build_index.py
```

#### Step 5: RAG Pipeline

```bash
python scripts/10_rag_pipeline.py
```

---

## 📊 Dashboard

```bash
streamlit run milestone4_dashboard.py
```

---

## 🧩 Milestones

* Milestone 1: Data preprocessing
* Milestone 2: Knowledge Graph
* Milestone 3: Semantic search & RAG
* Milestone 4: Dashboard

---

## 🛠️ Technologies Used

* Python, Pandas
* Neo4j
* FAISS + BM25
* LLM-based NER
* RAG Pipeline
* Streamlit / HTML / JS

---

## 📜 License

MIT License
