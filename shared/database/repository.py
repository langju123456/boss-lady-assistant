from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from shared.database.schema import connect


def upsert_daily_report(record: dict[str, Any]) -> dict[str, Any]:
    services = record.pop("services", {}) or {}
    report_date = record["date"]

    with connect() as conn:
        existing = conn.execute(
            "SELECT id FROM daily_reports WHERE date = ?", (report_date,)
        ).fetchone()

        if existing:
            report_id = existing["id"]
            conn.execute(
                """
                UPDATE daily_reports
                SET customers = ?, new_customers = ?, returning_customers = ?,
                    deals = ?, revenue = ?, notes = ?, raw_text = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    record.get("customers", 0),
                    record.get("new_customers"),
                    record.get("returning_customers"),
                    record.get("deals", 0),
                    record.get("revenue", 0),
                    record.get("notes"),
                    record.get("raw_text"),
                    report_id,
                ),
            )
            conn.execute("DELETE FROM services WHERE daily_report_id = ?", (report_id,))
        else:
            cursor = conn.execute(
                """
                INSERT INTO daily_reports (
                    date, customers, new_customers, returning_customers,
                    deals, revenue, notes, raw_text
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    report_date,
                    record.get("customers", 0),
                    record.get("new_customers"),
                    record.get("returning_customers"),
                    record.get("deals", 0),
                    record.get("revenue", 0),
                    record.get("notes"),
                    record.get("raw_text"),
                ),
            )
            report_id = cursor.lastrowid

        for service_name, quantity in services.items():
            conn.execute(
                """
                INSERT INTO services (daily_report_id, service_name, quantity)
                VALUES (?, ?, ?)
                """,
                (report_id, service_name, quantity),
            )

        row = conn.execute(
            "SELECT * FROM daily_reports WHERE id = ?", (report_id,)
        ).fetchone()
        saved = dict(row)
        saved["services"] = services
        return saved


def get_daily_report(report_date: date) -> dict[str, Any] | None:
    with connect() as conn:
        report = conn.execute(
            "SELECT * FROM daily_reports WHERE date = ?", (report_date.isoformat(),)
        ).fetchone()
        if not report:
            return None

        services = conn.execute(
            """
            SELECT service_name, quantity
            FROM services
            WHERE daily_report_id = ?
            ORDER BY quantity DESC
            """,
            (report["id"],),
        ).fetchall()
        data = dict(report)
        data["services"] = {row["service_name"]: row["quantity"] for row in services}
        return data


def get_reports_between(start_date: date, end_date: date) -> list[dict[str, Any]]:
    with connect() as conn:
        reports = conn.execute(
            """
            SELECT * FROM daily_reports
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC
            """,
            (start_date.isoformat(), end_date.isoformat()),
        ).fetchall()

        result = []
        for report in reports:
            services = conn.execute(
                """
                SELECT service_name, SUM(quantity) AS quantity
                FROM services
                WHERE daily_report_id = ?
                GROUP BY service_name
                ORDER BY quantity DESC
                """,
                (report["id"],),
            ).fetchall()
            data = dict(report)
            data["services"] = {
                row["service_name"]: row["quantity"] for row in services
            }
            result.append(data)
        return result


def get_recent_reports(days: int = 30) -> list[dict[str, Any]]:
    end_date = date.today()
    start_date = end_date - timedelta(days=days - 1)
    return get_reports_between(start_date, end_date)


def save_generated_content(topic: str, goal: str | None, content: dict[str, str]) -> None:
    with connect() as conn:
        for content_type, text in content.items():
            conn.execute(
                """
                INSERT INTO generated_content (topic, goal, content_type, content)
                VALUES (?, ?, ?, ?)
                """,
                (topic, goal, content_type, text),
            )


def save_advisor_log(question: str, answer: str) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO advisor_logs (question, answer) VALUES (?, ?)",
            (question, answer),
        )
