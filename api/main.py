from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Literal, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from agent_01_business_recorder.agent import BusinessRecorderAgent
from agent_02_business_analyst.agent import BusinessAnalystAgent
from agent_03_content_operator.agent import ContentOperatorAgent
from agent_04_business_advisor.agent import BusinessAdvisorAgent
from shared.database.schema import init_db
from shared.models.business import AdviceRequest, ContentRequest, RecordRequest

BASE_DIR = Path(__file__).resolve().parents[1]
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="老板娘经营助手", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

recorder = BusinessRecorderAgent()
analyst = BusinessAnalystAgent()
content_operator = ContentOperatorAgent()
advisor = BusinessAdvisorAgent()


@app.post("/api/record")
def record_business_report(payload: RecordRequest):
    return recorder.record(payload.text, report_date=payload.date)


@app.get("/api/reports/{period}")
def get_report(
    period: Literal["daily", "weekly", "monthly"],
    date_: Optional[date] = Query(default=None, alias="date"),
):
    target_date = date_ or date.today()
    if period == "daily":
        return analyst.daily_report(target_date)
    if period == "weekly":
        return analyst.weekly_report(target_date)
    return analyst.monthly_report(target_date)


@app.post("/api/content")
def generate_content(payload: ContentRequest):
    return content_operator.generate(payload.topic, payload.goal)


@app.post("/api/advice")
def ask_for_advice(payload: AdviceRequest):
    return advisor.advise(payload.question)


app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
