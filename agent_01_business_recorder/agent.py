from __future__ import annotations

from datetime import date
from typing import Any

from shared.database.repository import upsert_daily_report
from shared.tools.date_utils import resolve_chinese_date
from shared.tools.text_parser import (
    extract_money,
    extract_number_after_keywords,
    extract_services,
)


class BusinessRecorderAgent:
    """Converts owner voice/text reports into one daily database record."""

    def parse(self, text: str, report_date: date | None = None) -> dict[str, Any]:
        resolved_date = report_date or resolve_chinese_date(text)
        customers = extract_number_after_keywords(
            text, ["来了", "到店", "客人", "接待", "进店"]
        )
        deals = extract_number_after_keywords(text, ["成交", "成单", "开单", "买单"])
        new_customers = extract_number_after_keywords(text, ["新客", "新顾客"])
        returning_customers = extract_number_after_keywords(
            text, ["老客", "老顾客", "复购", "回头客"]
        )
        revenue = extract_money(text)
        services = extract_services(text)

        missing_fields = []
        if customers is None:
            missing_fields.append("今天来了几个客人")
        if deals is None:
            missing_fields.append("成交了几个")
        if revenue is None:
            missing_fields.append("收入多少钱")

        return {
            "date": resolved_date.isoformat(),
            "customers": customers or 0,
            "new_customers": new_customers,
            "returning_customers": returning_customers,
            "deals": deals or 0,
            "revenue": revenue or 0,
            "services": services,
            "notes": text,
            "raw_text": text,
            "missing_fields": missing_fields,
            "needs_follow_up": bool(missing_fields),
            "follow_up_question": self._follow_up_question(missing_fields),
        }

    def record(self, text: str, report_date: date | None = None) -> dict[str, Any]:
        parsed = self.parse(text, report_date)
        missing_fields = parsed.pop("missing_fields")
        needs_follow_up = parsed.pop("needs_follow_up")
        follow_up_question = parsed.pop("follow_up_question")
        saved = upsert_daily_report(parsed.copy())
        saved["missing_fields"] = missing_fields
        saved["needs_follow_up"] = needs_follow_up
        saved["follow_up_question"] = follow_up_question
        return saved

    def _follow_up_question(self, missing_fields: list[str]) -> str | None:
        if not missing_fields:
            return None
        return "还差一点：" + "、".join(missing_fields) + "？"
