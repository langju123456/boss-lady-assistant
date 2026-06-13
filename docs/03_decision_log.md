# Decision Log

Purpose:

Only major product and technical decisions.

Use this file when a decision changes product direction, architecture, or MVP scope.

Keep entries short.

Detailed lessons should go into `docs/06_lessons_learned.md`.

## Decisions

### #001

2026-06-13

Decision:
Do not start with RAG.

Reason:
Current user pain is not knowledge retrieval. The first pain is daily business recording and structured data collection.

### #002

2026-06-13

Decision:
Start with text input before voice input.

Reason:
Text input is easier to build and test. Voice input can be added later with Whisper.

### #003

2026-06-13

Decision:
Use SQLite first.

Reason:
The MVP is for one salon first. A local-first database is enough.

### #004

2026-06-13

Decision:
Do not build authentication, payment, or multi-tenant SaaS yet.

Reason:
The current goal is to validate one real user and one real workflow.

### #005

2026-06-13

Decision:
Build Business Recorder Agent first.

Reason:
User pain starts with daily business recording. Advice, reports, and content become more useful after the system has structured data.

