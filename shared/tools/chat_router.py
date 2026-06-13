from __future__ import annotations

from datetime import date
from typing import Any

from agent_01_business_recorder.agent import BusinessRecorderAgent
from agent_02_business_analyst.agent import BusinessAnalystAgent
from agent_03_content_operator.agent import ContentOperatorAgent
from agent_04_business_advisor.agent import BusinessAdvisorAgent
from shared.database.repository import get_daily_report
from shared.tools.formatters import (
    format_advice,
    format_daily_summary,
    format_marketing_content,
    format_record_confirmation,
)


class ChatRouter:
    def __init__(self) -> None:
        self.recorder = BusinessRecorderAgent()
        self.analyst = BusinessAnalystAgent()
        self.content_operator = ContentOperatorAgent()
        self.advisor = BusinessAdvisorAgent()

    def handle(self, message: str) -> dict[str, Any]:
        text = message.strip()
        intent = self.detect_intent(text)

        if intent == "summary":
            report = get_daily_report(date.today())
            return {
                "intent": intent,
                "reply": format_daily_summary(report),
                "data": report or {},
            }

        if intent == "marketing":
            content = self.content_operator.generate(topic=self.extract_topic(text))
            return {
                "intent": intent,
                "reply": format_marketing_content(content),
                "data": content,
            }

        if intent == "advice":
            advice = self.advisor.advise(text)
            return {
                "intent": intent,
                "reply": format_advice(advice),
                "data": advice,
            }

        record = self.recorder.record(text)
        return {
            "intent": "record",
            "reply": format_record_confirmation(record),
            "data": record,
        }

    def detect_intent(self, text: str) -> str:
        if any(keyword in text for keyword in ["查看", "今天数据", "今日数据", "汇总", "总结"]):
            return "summary"
        if any(keyword in text for keyword in ["活动", "文案", "朋友圈", "七夕", "促销", "通知"]):
            return "marketing"
        if any(keyword in text for keyword in ["怎么样", "怎么办", "建议", "分析", "生意", "不好", "下降"]):
            return "advice"
        return "record"

    def extract_topic(self, text: str) -> str:
        for keyword in ["帮我做", "做一个", "生成", "写一个"]:
            if keyword in text:
                topic = text.split(keyword, 1)[1].strip()
                if topic:
                    return topic
        return text or "门店活动"

