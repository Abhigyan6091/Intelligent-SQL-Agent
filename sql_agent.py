# sql_agent.py
import os
import re
import json
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

from llm_clients import OpenAIClient, MistralClient

load_dotenv()

DB_PATH = os.getenv("SQLITE_DB_PATH", "./example.db")
SQLITE_URI = f"sqlite:///{DB_PATH}"
MAX_ROWS = 1000

DANGEROUS_SQL = re.compile(r"\b(DROP|DELETE|UPDATE|INSERT|ALTER|TRUNCATE)\b", re.I)


def enforce_limit(sql: str):
    if sql.strip().lower().startswith("select") and "limit" not in sql.lower():
        return sql.rstrip(";") + f" LIMIT {MAX_ROWS};"
    return sql


def is_dangerous(sql: str):
    return bool(DANGEROUS_SQL.search(sql))


def discover_schema(engine):
    insp = inspect(engine)
    schema = {}
    for table in insp.get_table_names():
        cols = insp.get_columns(table)
        schema[table] = [(c["name"], str(c["type"])) for c in cols]
    return schema


def pick_tables(llm, question, schema):
    prompt = f"""
User question: {question}

Tables available: {list(schema.keys())}

Return ONLY a JSON list of table names that are relevant.
Example: ["users","orders"]
"""
    try:
        result = json.loads(llm.complete(prompt))
        return [t for t in result if t in schema]
    except:
        return list(schema.keys())  # fallback


def parse_intent(llm, question, tables):
    prompt = f"""
Question: {question}
Tables: {tables}

Return JSON with:
{{
  "intent": "select",
  "columns": [],
  "filters": [],
  "groupby": [],
  "orderby": null
}}
"""
    try:
        return json.loads(llm.complete(prompt))
    except:
        return {"intent": "select", "columns": [], "filters": [], "groupby": [], "orderby": None}


def generate_sql(llm, plan, tables):
    prompt = f"""
Generate a SAFE SQL query.

Plan:
{json.dumps(plan)}

Tables:
{tables}

Rules:
- ONLY produce SELECT
- NO UPDATE/DELETE/INSERT
- Use LIMIT if not provided
- Use :param placeholders only if needed
- Return ONLY SQL, no explanation
"""
    sql = llm.complete(prompt).strip().replace("```sql", "").replace("```", "")
    sql = enforce_limit(sql)
    if is_dangerous(sql):
        raise Exception("Dangerous SQL detected")
    return sql


def execute_sql(engine, sql: str):
    with engine.connect() as conn:
        rows = conn.execute(text(sql)).fetchmany(MAX_ROWS)
        return [dict(r) for r in rows]


def run_agent(question: str, provider="openai"):
    llm = OpenAIClient() if provider == "openai" else MistralClient()

    engine = create_engine(SQLITE_URI)

    schema = discover_schema(engine)
    candidates = pick_tables(llm, question, schema)
    plan = parse_intent(llm, question, candidates)
    sql = generate_sql(llm, plan, candidates)
    rows = execute_sql(engine, sql)

    return {
        "sql": sql,
        "rows": rows,
        "plan": plan,
        "tables_selected": candidates
    }
