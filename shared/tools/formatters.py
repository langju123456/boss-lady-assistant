from __future__ import annotations

from typing import Any


def money(value: Any) -> str:
    try:
        return f"{float(value):.0f}元"
    except (TypeError, ValueError):
        return "0元"


def int_value(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def format_record_confirmation(record: dict[str, Any]) -> str:
    lines = [
        "已记录今天数据：",
        f"营业额：{money(record.get('revenue'))}",
        f"客户数：{int_value(record.get('customers'))}",
        f"新客数：{int_value(record.get('new_customers'))}",
        f"老客数：{int_value(record.get('returning_customers'))}",
    ]
    if record.get("needs_follow_up") and record.get("follow_up_question"):
        lines.append("")
        lines.append(record["follow_up_question"])
    return "\n".join(lines)


def format_daily_summary(report: dict[str, Any] | None) -> str:
    if not report:
        return "今天还没有记录数据。你可以直接输入：今天来了8个客人收入3200。"

    return "\n".join(
        [
            "今日经营数据：",
            f"营业额：{money(report.get('revenue'))}",
            f"客户数：{int_value(report.get('customers'))}",
            f"新客数：{int_value(report.get('new_customers'))}",
            f"老客数：{int_value(report.get('returning_customers'))}",
        ]
    )


def format_marketing_content(content: dict[str, str]) -> str:
    if content.get("ai_generated"):
        return content["ai_generated"]
    return "\n\n".join(
        [
            f"活动方案：\n{content.get('promotion_details', '')}",
            f"朋友圈文案：\n{content.get('wechat_moments', '')}",
            f"客户通知文案：\n{content.get('follow_up_message', '')}",
        ]
    )


def format_advice(advice: dict[str, Any]) -> str:
    if advice.get("ai_generated"):
        return str(advice["ai_generated"])
    actions = advice.get("actions") or []
    action_text = "\n".join(f"{index}. {action}" for index, action in enumerate(actions, 1))
    if action_text:
        return f"{advice.get('summary', '')}\n\n建议：\n{action_text}"
    return str(advice.get("summary") or "现在数据还不够，先记录几天经营数据。")
