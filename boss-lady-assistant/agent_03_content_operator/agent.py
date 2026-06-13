from __future__ import annotations

from shared.database.repository import save_generated_content


class ContentOperatorAgent:
    def generate(self, topic: str, goal: str | None = None) -> dict[str, str]:
        goal_text = goal or "拉新和复购"
        clean_topic = topic.removesuffix("活动")
        content = {
            "campaign_theme": f"{clean_topic}美丽宠爱计划",
            "promotion_details": (
                f"目标：{goal_text}。建议设置3天预热、2天集中成交。"
                "主推一个高感知项目，搭配到店小礼，老顾客可带朋友同享体验价。"
            ),
            "poster_copy": (
                f"{clean_topic}限时活动\n"
                "给自己一次认真变美的机会\n"
                "到店体验护理，提前预约享专属礼遇"
            ),
            "wechat_moments": (
                f"{clean_topic}活动开始啦。\n"
                "最近很多姐妹都说皮肤状态不稳定，我们这次准备了适合日常保养的护理方案。"
                "想改善、想试试、想带朋友一起来，都可以私信我预约。名额不多，先到先约。"
            ),
            "video_script": (
                "开头：姐妹们，最近是不是觉得皮肤暗沉、缺水、上妆不服帖？\n"
                f"中间：我们店这次做{clean_topic}活动，重点帮你做一次皮肤状态调整。\n"
                "结尾：想预约的姐妹直接私信我，给你留时间。"
            ),
            "follow_up_message": (
                "姐，今天护理后皮肤状态会慢慢稳定，今晚先不要熬夜，也别用刺激产品。"
                "明天我再问你一下感觉，如果合适可以帮你安排下一次。"
            ),
            "referral_campaign": (
                "老顾客带一位新朋友到店，两人都送一次基础补水护理升级。"
                "朋友成交后，老顾客再送项目抵扣券。"
            ),
        }
        save_generated_content(topic, goal, content)
        return content
