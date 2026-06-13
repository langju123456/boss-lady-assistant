from __future__ import annotations

from agent_02_business_analyst.agent import BusinessAnalystAgent
from shared.database.repository import get_recent_reports, save_advisor_log


class BusinessAdvisorAgent:
    def __init__(self) -> None:
        self.analyst = BusinessAnalystAgent()

    def advise(self, question: str) -> dict[str, str | list[str]]:
        reports = get_recent_reports(30)
        metrics = self.analyst._metrics(reports)
        answer = self._answer(question, metrics)
        save_advisor_log(question, answer["summary"])
        return answer

    def _answer(self, question: str, metrics: dict) -> dict[str, str | list[str]]:
        if metrics["customers"] == 0:
            return {
                "summary": "现在数据还不够，先连续记录7天经营日报，系统才能判断是客流、成交还是复购的问题。",
                "actions": [
                    "每天用一句话记录到店人数、成交人数、收入",
                    "尽量补充新客和老客数量",
                    "先做一个老顾客回访，问最近皮肤状态",
                ],
            }

        actions = []
        if "不好" in question or "差" in question or "没客" in question:
            actions.extend(
                [
                    "先做老顾客唤醒：给30天没来的顾客发护理提醒",
                    "发一个转介绍活动：老客带新客，两人都有护理升级",
                    "连续3天发真实案例朋友圈，不要只发硬广告",
                ]
            )
        elif "活动" in question or "促销" in question:
            actions.extend(
                [
                    "只主推一个项目，别同时推太多",
                    "设置限时预约名额，让顾客容易做决定",
                    "活动结束后马上追踪未成交顾客",
                ]
            )
        else:
            actions.extend(
                [
                    "保持每天记录经营数据",
                    "优先提升成交率，再考虑加大引流",
                    "把表现最好的项目做成固定套餐",
                ]
            )

        summary = (
            f"近30天到店{metrics['customers']}人，成交{metrics['deals']}单，"
            f"收入{metrics['revenue']:.0f}元，成交率{metrics['conversion_rate']:.0f}%。"
        )
        if metrics["conversion_rate"] < 50:
            summary += " 主要问题可能在成交，不是单纯没流量。"
        elif metrics["new_customers"] == 0:
            summary += " 目前缺少新客数据，建议开始区分新客和老客。"
        else:
            summary += " 可以围绕老顾客复购和转介绍继续放大。"

        return {"summary": summary, "actions": actions}
