# 老板娘经营助手

A voice-first AI business assistant for small beauty salon owners in China.

## Current MVP Goal

Help one real salon owner record daily business data through natural language input.

The first usable demo is designed for the founder's mother to test this week.

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
.
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

## Knowledge Management System

Record once. Reuse everywhere.

```text
Product Journal
+
Customer Discovery
+
Decision Log
↓
Lessons Learned
↓
Build In Public
↓
LinkedIn / Blog / Interview Stories
```

The founder should primarily maintain:

```text
docs/06_lessons_learned.md
```

Then regenerate the public story:

```bash
python3 scripts/process_lessons.py
```

## Quick Start

### Streamlit Demo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Open:

```text
http://localhost:8501
```

### FastAPI Backend

```bash
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

Without `OPENAI_API_KEY`, the app still works with local rule-based parsing, templates, summaries, and advice.

## MVP User Flow

The salon owner opens one URL and types naturally:

```text
今天来了8个客人收入3200新客4个老客4个
```

The system replies:

```text
已记录今天数据
营业额：3200元
客户数：8
新客数：4
老客数：4
```

Then she can ask:

```text
帮我做七夕活动
```

The system returns:

- 活动方案
- 朋友圈文案
- 客户通知文案

## Deployment

### Render

1. Push this repo to GitHub.
2. Create a new Render Web Service.
3. Use this repository.
4. Build command:

```bash
pip install -r requirements.txt
```

5. Start command:

```bash
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

6. Add environment variables:

```text
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
BOSS_LADY_DB_PATH=shared/database/boss_lady.sqlite3
```

`render.yaml` is also included for Render Blueprint deployment.

### Railway

1. Create a new Railway project from this GitHub repo.
2. Add the same environment variables.
3. Use this start command:

```bash
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0
```

## API

- `POST /api/record` - record a natural language business report
- `POST /api/chat` - one-message chat router for record, summary, content, and advice
- `GET /api/summary/today` - today summary
- `GET /api/reports/daily?date=YYYY-MM-DD` - daily report
- `GET /api/reports/weekly?date=YYYY-MM-DD` - weekly report ending on date
- `GET /api/reports/monthly?date=YYYY-MM-DD` - month report
- `POST /api/content` - generate marketing content
- `POST /api/advice` - ask business questions naturally
