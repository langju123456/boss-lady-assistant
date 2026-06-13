from __future__ import annotations

from datetime import date, timedelta


def resolve_chinese_date(text: str, fallback: date | None = None) -> date:
    base = fallback or date.today()
    if "前天" in text:
        return base - timedelta(days=2)
    if "昨天" in text:
        return base - timedelta(days=1)
    if "明天" in text:
        return base + timedelta(days=1)
    return base


def month_bounds(target_date: date) -> tuple[date, date]:
    start = target_date.replace(day=1)
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1)
    else:
        next_month = start.replace(month=start.month + 1)
    return start, next_month - timedelta(days=1)


def week_bounds(target_date: date) -> tuple[date, date]:
    start = target_date - timedelta(days=target_date.weekday())
    return start, start + timedelta(days=6)
