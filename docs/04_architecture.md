# Architecture

Purpose:

Technical evolution only.

Use this file for agent architecture, database changes, system design, and future technical roadmap.

Product lessons should go into `docs/06_lessons_learned.md`.

## Current MVP Architecture

User input:
Text first, voice later.

Flow:

```text
Natural language input
-> Business Recorder Agent
-> Structured data extraction
-> SQLite database
-> Business Analyst Agent
-> Daily / weekly / monthly report
-> Business Advisor Agent
-> Simple recommendation
```

## Agent Modules

### Agent 01: Business Recorder Agent

Goal:
Convert natural language daily reports into structured business records.

### Agent 02: Business Analyst Agent

Goal:
Analyze daily, weekly, and monthly business performance.

### Agent 03: Content Operator Agent

Goal:
Generate WeChat Moments posts, campaign plans, short-video scripts, customer follow-up messages, and promotion copy.

### Agent 04: Business Advisor Agent

Goal:
Act as the main AI business advisor that uses data and content tools to answer business questions.

## Database

Use SQLite first.

Initial tables:

* daily_reports
* services
* generated_content
* advisor_logs

## Future Architecture

* Add Whisper for voice input
* Add LangGraph for multi-agent orchestration
* Add RAG only when historical activity plans, customer notes, and business documents become useful
* Add WeChat integration later
* Add dashboard later

## Product Architecture Principle: 2026-06-13

The current architecture is:

```text
Business Recorder Agent
↓
Business Analyst Agent
↓
Content Operator Agent
↓
Business Advisor Agent
```

The future user experience should be:

```text
One chat window.
The owner talks naturally.
The system coordinates multiple agents behind the scenes.
```

Frontend should be simple.

Backend can become complex.

The owner should not need to understand agents, databases, dashboards, RAG, or orchestration.

The product should feel like one conversation, even if the system behind it becomes multi-agent.
