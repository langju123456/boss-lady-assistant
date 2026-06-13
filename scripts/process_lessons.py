from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LESSONS_PATH = ROOT / "docs" / "06_lessons_learned.md"
BUILD_IN_PUBLIC_PATH = ROOT / "docs" / "05_build_in_public.md"

FIELDS = [
    "Date",
    "Original Assumption",
    "New Insight",
    "Evidence",
    "Why It Matters",
    "Product Decision",
    "LinkedIn Angle",
]


@dataclass
class Lesson:
    date: str
    original_assumption: str
    new_insight: str
    evidence: str
    why_it_matters: str
    product_decision: str
    linkedin_angle: str


def parse_lessons(markdown: str) -> list[Lesson]:
    lessons = []
    for block in markdown.split("---"):
        values = parse_block(block)
        if not values.get("Date") or not values.get("Original Assumption"):
            continue
        lessons.append(
            Lesson(
                date=values.get("Date", ""),
                original_assumption=values.get("Original Assumption", ""),
                new_insight=values.get("New Insight", ""),
                evidence=values.get("Evidence", ""),
                why_it_matters=values.get("Why It Matters", ""),
                product_decision=values.get("Product Decision", ""),
                linkedin_angle=values.get("LinkedIn Angle", ""),
            )
        )
    return sorted(lessons, key=lambda lesson: lesson.date)


def parse_block(block: str) -> dict[str, str]:
    values: dict[str, list[str]] = {field: [] for field in FIELDS}
    current_field: str | None = None

    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        matched_field = next((field for field in FIELDS if line == f"{field}:"), None)
        if matched_field:
            current_field = matched_field
            continue

        if current_field:
            values[current_field].append(line)

    return {field: " ".join(lines).strip() for field, lines in values.items()}


def render_build_in_public(lessons: list[Lesson]) -> str:
    lines = [
        "# Build in Public",
        "",
        "<!-- AUTO-GENERATED: Do not edit manually. Update docs/06_lessons_learned.md and run scripts/process_lessons.py. -->",
        "",
        "Purpose:",
        "",
        "Convert lessons into a public founder narrative.",
        "",
        "This file is generated from:",
        "",
        "```text",
        "docs/06_lessons_learned.md",
        "```",
        "",
        "Future uses:",
        "",
        "* LinkedIn posts",
        "* Blog posts",
        "* PM interview stories",
        "* Startup case studies",
        "* Founder reflections",
        "",
        "## Public Founder Story",
        "",
    ]

    for lesson in lessons:
        lines.extend(
            [
                f"### {lesson.date}",
                "",
                "What I Thought",
                "",
                lesson.original_assumption,
                "",
                "What I Learned",
                "",
                lesson.new_insight,
                "",
                "What Changed",
                "",
                lesson.product_decision,
                "",
                "What I'm Building Now",
                "",
                infer_current_build(lesson),
                "",
                "Why It Matters",
                "",
                lesson.why_it_matters,
                "",
                "Public Angle",
                "",
                lesson.linkedin_angle,
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def infer_current_build(lesson: Lesson) -> str:
    decision = lesson.product_decision.strip()
    if decision:
        return decision
    return "Turning the lesson into a smaller, more useful product decision."


def main() -> None:
    lessons = parse_lessons(LESSONS_PATH.read_text(encoding="utf-8"))
    BUILD_IN_PUBLIC_PATH.write_text(render_build_in_public(lessons), encoding="utf-8")
    print(f"Generated {BUILD_IN_PUBLIC_PATH} from {len(lessons)} lessons.")


if __name__ == "__main__":
    main()

