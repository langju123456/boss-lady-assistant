# 老板娘经营助手

A voice-first AI business assistant for small beauty salon owners.

## Current MVP Goal

Help one real salon owner record daily business data through natural language input.

## Core Workflow

```text
Text or voice input
→ Structured business data
→ SQLite database
→ Business report
→ Business advice
```

The owner can type a natural business update, and the system will:

- Extract structured daily business data
- Save it to SQLite
- Generate daily, weekly, and monthly reports
- Create ready-to-use marketing content
- Give plain-language business advice

Phase 1 is intentionally small: one salon, no login, no CRM, no payments.

## Four Agents

1. Business Recorder Agent
2. Business Analyst Agent
3. Content Operator Agent
4. Business Advisor Agent

## Project Structure

```text
boss-lady-assistant/
├── agent_01_business_recorder/
├── agent_02_business_analyst/
├── agent_03_content_operator/
├── agent_04_business_advisor/
├── shared/
│   ├── database/
│   ├── models/
│   ├── prompts/
│   └── tools/
├── api/
├── frontend/
├── docs/
└── README.md
```

## Documentation

* [Vision](docs/00_vision.md)
* [Product Journal](docs/01_product_journal.md)
* [Customer Discovery](docs/02_customer_discovery.md)
* [Decision Log](docs/03_decision_log.md)
* [Architecture](docs/04_architecture.md)
* [Build in Public](docs/05_build_in_public.md)
* [Lessons Learned](docs/06_lessons_learned.md)
* [LinkedIn Post Generator Prompt](docs/linkedin_post_prompt.md)

## Quick Start

```bash
cd boss-lady-assistant
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## Example Input

```text
今天来了8个客人，成交5个，收入3200元，其中祛斑2个，补水3个。
```

Example response:

```json
{
  "customers": 8,
  "deals": 5,
  "revenue": 3200,
  "services": {
    "祛斑": 2,
    "补水": 3
  }
}
```

## Optional OpenAI Setup

The MVP works with local rule-based Chinese parsing. To add AI generation/parsing later:

```bash
cp .env.example .env
export OPENAI_API_KEY="your_api_key"
```

## API

- `POST /api/record` - record a natural language business report
- `GET /api/reports/daily?date=YYYY-MM-DD` - daily report
- `GET /api/reports/weekly?date=YYYY-MM-DD` - weekly report ending on date
- `GET /api/reports/monthly?date=YYYY-MM-DD` - month report
- `POST /api/content` - generate marketing content
- `POST /api/advice` - ask business questions naturally
