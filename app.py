from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pyngrok import ngrok
import uvicorn
import threading
import json

from yahooquery import search as yq_search
from crewai import Crew, Process
from tasks import (
    get_company_news_task,
    analyze_stock_task,
    investment_decision_task
)
from agents import (
    log_analyzer,
    stock_analysis_agent,
    investment_advisor_agent
)

# Start ngrok tunnel
# public_url = ngrok.connect(5000)
# print("Public URL:", public_url)


app = FastAPI(title="AI Stock Analyzer")

# Serve the single-page frontend
@app.get("/", response_class=HTMLResponse)
def home():
    return Path("index.html").read_text(encoding="utf-8")

# Autocomplete search using yahooquery
@app.get("/search")
def search_companies(q: str = Query(..., min_length=1)):
    results = yq_search(q)
    quotes = results.get("quotes", []) or []
    return [
        {"name": r.get("shortname"), "symbol": r.get("symbol")}
        for r in quotes
        if r.get("quoteType") == "EQUITY" and r.get("shortname") and r.get("symbol")
    ]

# Analyze endpoint: runs CrewAI pipeline and returns structured sections
@app.get("/analyze")
def analyze(company: str = Query(..., description="Company name")):
    crew = Crew(
        agents=[log_analyzer, stock_analysis_agent, investment_advisor_agent],
        tasks=[get_company_news_task, analyze_stock_task, investment_decision_task],
        process=Process.sequential,
        verbose=True
    )

    # Kick off the workflow; each task returns content in memory via CrewAI
    result = crew.kickoff(inputs={"company_name": company})

    # Expect investment_advisor_agent final output as string
    recommendation_text = str(result)

    # Retrieve the last outputs from the first two tasks via their memory/context
    # Depending on CrewAI version, tasks may expose output in .output or agent memory.
    # We'll safely extract from the task objects (they’re referenced in context).
    news_summary = getattr(get_company_news_task, "output", None) or ""
    financials_structured = getattr(analyze_stock_task, "output", None)

    # Normalize structured financials into a dict; fallback to empty dict
    try:
        financials = json.loads(financials_structured) if isinstance(financials_structured, str) else financials_structured
    except Exception:
        financials = {"raw": str(financials_structured or "")}

    if not isinstance(financials, dict):
        financials = {"raw": str(financials)}

    return {
        "financials": financials,
        "news": str(news_summary),
        "recommendation": recommendation_text
    }

# Run Uvicorn in background thread
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

