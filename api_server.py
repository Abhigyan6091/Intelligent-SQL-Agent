# api_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

from sql_agent import run_agent

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    llm_provider: str = "openai"

@app.post("/query")
def query(req: QueryRequest):
    try:
        out = run_agent(req.question, llm_provider=req.llm_provider)
        return out
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run:
# uvicorn api_server:app --reload --port 8000
