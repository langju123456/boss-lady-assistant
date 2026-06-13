from __future__ import annotations

import re


SERVICE_STOP_WORDS = {
    "来了",
    "客人",
    "成交",
    "收入",
    "其中",
    "今天",
    "昨天",
    "前天",
    "新客",
    "老客",
    "复购",
}


def extract_number_after_keywords(text: str, keywords: list[str]) -> int | None:
    keyword_pattern = "|".join(re.escape(keyword) for keyword in keywords)
    patterns = [
        rf"(?:{keyword_pattern})\D{{0,6}}(\d+)",
        rf"(\d+)\s*(?:个|位|名)?\s*(?:{keyword_pattern})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def extract_money(text: str) -> float | None:
    patterns = [
        r"(?:收入|营业额|收款|业绩|卖了|做到)\D{0,6}(\d+(?:\.\d+)?)\s*(?:元|块|块钱|人民币)?",
        r"(\d+(?:\.\d+)?)\s*(?:元|块|块钱)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return float(match.group(1))
    return None


def extract_services(text: str) -> dict[str, int]:
    services: dict[str, int] = {}
    normalized = text.replace("，", ",").replace("。", ",").replace("、", ",")
    for part in normalized.split(","):
        if not any(marker in part for marker in ["个", "次", "单"]):
            continue
        for name, qty in re.findall(r"([\u4e00-\u9fa5A-Za-z]{2,12})\s*(\d+)\s*(?:个|次|单)", part):
            clean_name = name.strip("其中做了来了成交收入")
            if clean_name and clean_name not in SERVICE_STOP_WORDS:
                services[clean_name] = services.get(clean_name, 0) + int(qty)
    return services
