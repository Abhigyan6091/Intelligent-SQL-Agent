🚀 Intelligent SQL Agent (OpenAI / Mistral)

A natural-language to SQL agent that converts plain English questions into safe SQL queries, automatically identifies relevant tables, executes the query, and returns results — all powered by LLMs and a sample SQLite database.

This repo contains:

A lightweight SQL agent

OpenAI & Mistral LLM clients

A sample SQLite database

A FastAPI server for querying the agent

Safety layers (read-only SQL, SQL validation, LIMIT enforcement)

📦 Features

✔ Ask questions in plain English
✔ Automatically identifies relevant tables
✔ LLM-based SQL generation (OpenAI or Mistral)
✔ Prevents harmful SQL (DROP, DELETE, UPDATE, etc.)
✔ Automatically inserts LIMIT to avoid full table scans
✔ Outputs SQL + query results + internal plan
✔ Includes sample database (users, orders)



🔧 Requirements

Python 3.10+

An API key for:

OpenAI, or

Mistral (optional)

Install dependencies:

pip install -r requirements.txt



🛠️ Create the Sample Database

Run:

python create_sample_db.py


This generates example.db with:

users

| id | name | email | signup_date |

orders

| id | user_id | amount | created_at | status |

▶️ Run the API Server

Start the FastAPI backend:

uvicorn api_server:app --reload --port 8000


Open your browser:

http://127.0.0.1:8000/docs


You now see an interactive UI where you can test the SQL agent.

🤖 How to Query the Agent

POST to:

POST /query


Example request:

{
  "question": "Show total completed orders per user",
  "llm_provider": "openai"
}


Example response:

{
  "sql": "SELECT u.name, COUNT(o.id) AS total_orders FROM users u JOIN orders o ON o.user_id=u.id WHERE o.status='completed' LIMIT 1000;",
  "rows": [
    { "name": "Alice", "total_orders": 2 },
    { "name": "Charlie", "total_orders": 1 }
  ],
  "tables_selected": ["users", "orders"],
  "plan": {
    "intent": "select",
    "columns": [],
    "filters": [],
    "groupby": [],
    "orderby": null
  }
}

🧠 Architecture Overview
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

🔒 Security Measures

The agent will NOT execute:

DROP TABLE

DELETE / UPDATE

INSERT

ALTER

TRUNCATE

All queries must begin with SELECT.

Every output is automatically wrapped with:

LIMIT 1000

💬 Example Questions You Can Ask

“List all users who signed up after 2024”

“Give me total revenue per user”

“How many completed orders does Alice have?”

“Show pending vs completed order counts”

“What is the average order amount per user?”

🧪 Curl Example
curl -X POST "http://127.0.0.1:8000/query" \
-H "Content-Type: application/json" \
-d "{\"question\": \"list all users\", \"llm_provider\": \"openai\"}"

🐛 Troubleshooting
❌ openai.OpenAI is not working

Install latest:

pip install --upgrade openai

❌ no such table: users

You forgot:

python create_sample_db.py

❌ “Dangerous SQL detected”

The LLM attempted non-SELECT SQL.
Try rephrasing the question.

❌ LLM not returning JSON

You can add few-shot examples in prompts for stability.

📘 Future Enhancements

🚀 Add LangGraph DAG visualization
🚀 Add fully reactive web UI
🚀 Add PostgreSQL/MySQL adapters
🚀 Add SQL cost estimation (EXPLAIN)
🚀 Add schema embeddings for better table selection