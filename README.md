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

pip install -r requirements.txt



# 🧠 SQL Agent Architecture & Features

## 🏗️ Architecture Overview

The SQL Agent follows a modular, multi-step pipeline that transforms natural-language queries into safe, validated SQL commands. The entire system is LLM-driven, schema-aware, and safety-focused.

### **1. Schema Discovery**
- Reads table names, column names, and types using SQLAlchemy.
- Automatically adapts to database structure.
- Provides context for downstream LLM reasoning.

### **2. Table Relevance Selection (LLM-Assisted)**
- LLM analyzes the user's question.
- Identifies which tables are relevant.
- Ensures SQL generation is grounded in the actual schema.

### **3. Intent Parsing (LLM)**
Converts the natural-language question into a structured JSON plan:
- `intent`: select / aggregate  
- `columns`: list of fields  
- `filters`: conditions the user asked for  
- `groupby`: grouping fields  
- `orderby`: sorting preferences  

This structured format ensures predictable SQL generation.

### **4. SQL Generation (LLM)**
- LLM produces SQL based on the structured plan + schema.
- Uses only **safe, read-only SQL**.
- Parameters use named placeholders (`:p1`, `:p2`) when needed.

### **5. Safety Layer**
Before executing SQL:
- Blocks dangerous keywords: `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, `TRUNCATE`.
- Auto-adds a `LIMIT` clause if missing.
- Ensures query begins with `SELECT`.
- Verifies SQL structure.

### **6. Execution Layer**
- Safely executes SQL against the SQLite database.
- Returns up to `MAX_ROWS` rows.
- Converts results into Python dicts for JSON output.

### **7. Result Packaging**
Response contains:
- Generated SQL
- Query results
- Selected tables
- The interpreted plan (intents, filters, etc.)

This provides full transparency into how the agent reasoned.

---

## ✨ Key Features

### ✔ **Natural Language → SQL**
Ask questions such as:
- “Show total sales per customer.”
- “List users who signed up after 2024.”

The agent generates correct, executable SQL automatically.

---

### ✔ **Automatic Schema Awareness**
- No need to hardcode column names or table relationships.
- Updates automatically if database schema changes.

---

### ✔ **Supports Multiple LLMs**
- **OpenAI models** (e.g. `gpt-4o-mini`)
- **Mistral models** (e.g. `mistral-small-latest`)

Switch LLM using one parameter:
```json
"llm_provider": "openai"









