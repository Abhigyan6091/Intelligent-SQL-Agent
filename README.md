# 🚀 Intelligent SQL Agent (OpenAI / Mistral)

A natural-language SQL agent that converts plain English questions into safe SQL queries, automatically identifies relevant tables, executes the generated SQL, and returns structured results.

Powered by **OpenAI** or **Mistral** LLMs + a sample **SQLite** database.

---

## 📦 Features

- ✔ Ask questions in **plain English**
- ✔ Automatically identifies **relevant tables**
- ✔ Generates **safe SQL** using LLMs
- ✔ Prevents harmful SQL (`DROP`, `DELETE`, `UPDATE`, etc.)
- ✔ Automatically applies `LIMIT` to avoid full scans
- ✔ Returns SQL, rows, internal plan, selected tables
- ✔ Comes with a prebuilt **sample DB (`users`, `orders`)**

---





---

## 🔧 Requirements

- Python **3.10+**
- API Key for:
  - 🔑 **OpenAI** (recommended), or  
  - 🔑 **Mistral**

Install dependencies:

```bash
pip install -r requirements.txt





## ▶️ Run the API Server

Start the FastAPI backend:

uvicorn api_server:app --reload --port 8000


Open your browser:

**http://127.0.0.1:8000/docs**


You now see an interactive UI where you can test the SQL agent.


## 🧠 Architecture Overview
   1️⃣ Schema Discovery

   Reads column names & table structure from SQLite.

  2️⃣ Table Relevance (LLM)

  Decides which tables matter for the query.

  3️⃣ Intent Parsing (LLM)

  Maps user question → structured plan (JSON).

  4️⃣ SQL Generation (LLM)

  LLM creates a safe SQL query.

  5️⃣ Safety Layer

  Blocks destructive SQL

  Enforces SELECT-only

  Auto-adds LIMIT

  6️⃣ Database Execution

  Runs SQL safely, returns rows.



## 📘 Future Enhancements

🚀 Add LangGraph DAG visualization
🚀 Add fully reactive web UI
🚀 Add PostgreSQL/MySQL adapters
🚀 Add SQL cost estimation (EXPLAIN)

🚀 Add schema embeddings for better table selection

