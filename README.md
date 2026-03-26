 Enterprise Knowledge Graph Project
 Project Overview

This project builds a complete Enterprise Knowledge Graph System from raw customer data to an intelligent, queryable system.

It includes:

Data ingestion and preprocessing
Entity creation & LLM-based Named Entity Recognition (NER)
Knowledge Graph construction in Neo4j
Semantic search (FAISS + BM25)
RAG (Retrieval-Augmented Generation) pipeline
Interactive dashboard UI

System Workflow
Raw Data (data_raw/*.csv)
         ↓
01_load_raw_data.py → 02_data_profiling.py → 03_preprocess_data.py
         ↓
04_create_entities.py → Create Entity CSVs (kg_*.csv)
         ↓
05_load_to_neo4j.py → Load entities into Neo4j
         ↓
06_apply_llm_ner.py → Extract entities & relationships
         ↓
07_create_embeddings.py → Create vector embeddings
         ↓
08_test_search.py → Test semantic search
         ↓
09_build_index.py → Build search index
         ↓
10_rag_pipeline.py → RAG pipeline for intelligent answers
         ↓
API / Frontend Dashboard

Repository Structure

ai-knowledge-graph-internship/
│
├── .vscode/               # VS Code settings
├── data_raw/              # Original dataset
│   ├── dim_customer.csv
│   ├── dim_product.csv
│   └── fact_order.csv
├── data_staging/          # Processed & KG-ready CSVs
│   ├── clean_customers.csv    # Cleaned customer data
│   ├── clean_products.csv     # Cleaned product data
│   ├── clean_orders.csv       # Cleaned order data
│   ├── kg_customers.csv       # Entity table for KG
│   ├── kg_products.csv        # Entity table for KG
│   ├── kg_orders.csv          # Entity table for KG
│   ├── llm_customers.csv      # NER results for customers
│   └── llm_products.csv       # NER results for products
├── scripts/               # Core pipeline scripts
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
├── momndaughtereatsdp.jpeg   # Dashboard / example image
├── README.md
├── requirements.txt
├── license.txt
└── .gitignore 

How to Run the Project
1️) Clone Repo
git clone https://github.com/Sherin-Suresh/ai-knowledge-graph-internship.git
cd ai-knowledge-graph-internship

2)Create Virtual Environment
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate   # Linux / Mac

3)Install Dependencies
pip install -r requirements.txt

4)Run Scripts in Order
Step 1: Data Loading & Preprocessing
python scripts/01_load_raw_data.py
python scripts/02_data_profiling.py
python scripts/03_preprocess_data.py

Step 2: Create Entities & Load to Neo4j
python scripts/04_create_entities.py
python scripts/05_load_to_neo4j.py

Step 3: Apply LLM NER & Create Embeddings
python scripts/06_apply_llm_ner.py
python scripts/07_create_embeddings.py

Step 4: Test Search & Build Index
python scripts/08_test_search.py
python scripts/09_build_index.py

Step 5: Run RAG Pipeline
python scripts/10_rag_pipeline.py

5️) Dashboard
streamlit run milestone4_dashboard.py

Milestones
Milestone 1: Data ingestion & preprocessing → clean_*.csv
Milestone 2: Entity extraction & KG building → kg_*.csv, llm_*.csv
Milestone 3: Semantic search & RAG pipelines
Milestone 4: Dashboard & deployment

Technologies Used
Python, Pandas
Neo4j
FAISS + BM25
LLM-based NER
RAG pipeline
HTML / JavaScript (dashboard UI)

License
MIT License
