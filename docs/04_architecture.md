# Architecture

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

