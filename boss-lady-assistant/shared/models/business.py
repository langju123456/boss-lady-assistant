from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class RecordRequest(BaseModel):
    text: str = Field(..., min_length=1, description="老板娘自然语言经营日报")
    date: Optional[date] = None


class ContentRequest(BaseModel):
    topic: str = Field(..., min_length=1, description="活动或内容主题")
    goal: Optional[str] = Field(default=None, description="例如拉新、复购、转介绍")


class AdviceRequest(BaseModel):
    question: str = Field(..., min_length=1, description="自然语言经营问题")
