from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
from typing import Any

from shared.database.repository import get_daily_report, get_reports_between
from shared.tools.date_utils import month_bounds, week_bounds


class BusinessAnalystAgent:
    def daily_report(self, target_date: date) -> dict[str, Any]:
        report = get_daily_report(target_date)
        if not report:
            return {
                "period": "daily",
                "date": target_date.isoformat(),
                "summary": "今天还没有记录经营数据。",
                "metrics": {},
                "recommendation": "先发一条今天的经营情况，例如：今天来了8个客人，成交5个，收入3200元。",
            }
        return self._build_report("daily", target_date, target_date, [report])

    def weekly_report(self, target_date: date) -> dict[str, Any]:
        start, end = week_bounds(target_date)
        current = get_reports_between(start, end)
        previous = get_reports_between(start - timedelta(days=7), end - timedelta(days=7))
        return self._build_report("weekly", start, end, current, previous)

    def monthly_report(self, target_date: date) -> dict[str, Any]:
        start, end = month_bounds(target_date)
        current = get_reports_between(start, end)
        previous_end = start - timedelta(days=1)
        previous_start, _ = month_bounds(previous_end)
        previous = get_reports_between(previous_start, previous_end)
        return self._build_report("monthly", start, end, current, previous)

    def _build_report(
        self,
        period: str,
        start: date,
        end: date,
        reports: list[dict[str, Any]],
        previous_reports: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        metrics = self._metrics(reports)
        previous_metrics = self._metrics(previous_reports or [])
        revenue_change = self._percent_change(
            metrics["revenue"], previous_metrics["revenue"]
        )
        top_service = metrics["top_services"][0][0] if metrics["top_services"] else None

        summary = (
            f"{start.isoformat()} 至 {end.isoformat()}：收入{metrics['revenue']:.0f}元，"
            f"到店{metrics['customers']}人，成交{metrics['deals']}单，"
            f"转化率{metrics['conversion_rate']:.0f}%。"
        )
        if revenue_change is not None:
            direction = "增加" if revenue_change >= 0 else "下降"
            summary += f"收入比上期{direction}{abs(revenue_change):.0f}%。"

        recommendation = self._recommend(metrics, revenue_change, top_service)
        return {
            "period": period,
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
            "summary": summary,
            "metrics": metrics,
            "comparison": {"revenue_change_percent": revenue_change},
            "recommendation": recommendation,
        }

    def _metrics(self, reports: list[dict[str, Any]]) -> dict[str, Any]:
        revenue = sum(float(row.get("revenue") or 0) for row in reports)
        customers = sum(int(row.get("customers") or 0) for row in reports)
        deals = sum(int(row.get("deals") or 0) for row in reports)
        new_customers = sum(int(row.get("new_customers") or 0) for row in reports if row.get("new_customers") is not None)
        returning_customers = sum(int(row.get("returning_customers") or 0) for row in reports if row.get("returning_customers") is not None)

        services = Counter()
        for report in reports:
            services.update(report.get("services") or {})

        conversion_rate = (deals / customers * 100) if customers else 0
        returning_rate = (
            returning_customers / customers * 100
            if customers and returning_customers
            else 0
        )
        return {
            "revenue": revenue,
            "customers": customers,
            "deals": deals,
            "new_customers": new_customers,
            "returning_customers": returning_customers,
            "conversion_rate": conversion_rate,
            "returning_customer_rate": returning_rate,
            "top_services": services.most_common(5),
        }

    def _percent_change(self, current: float, previous: float) -> float | None:
        if previous <= 0:
            return None
        return (current - previous) / previous * 100

    def _recommend(
        self, metrics: dict[str, Any], revenue_change: float | None, top_service: str | None
    ) -> str:
        if metrics["customers"] == 0:
            return "先把每天到店、成交、收入记起来，连续记7天后建议会更准。"
        if metrics["conversion_rate"] < 50:
            return "成交率偏低，明天重点练一个主推项目的话术，并给到店顾客一个限时小套餐。"
        if revenue_change is not None and revenue_change < -10:
            return "收入在下滑，建议做老顾客唤醒：发3天护理提醒，加一个到店小礼。"
        if top_service:
            return f"{top_service}表现最好，下周可以围绕它做一个套餐和朋友圈案例。"
        return "经营状态正常，继续记录数据，并补充新客和老客数量。"
